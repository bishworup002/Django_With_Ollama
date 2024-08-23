import ollama
from django.core.management.base import BaseCommand
from properties.models import Property, PropertySummary


class Command(BaseCommand):
    help = "Generate descriptions and summaries for properties"

    def handle(self, *args, **kwargs):
        properties = Property.objects.all()
        self.stdout.write(self.style.NOTICE(f"Found {properties.count()} properties."))

        for property in properties:
            title = property.title
            locations = ", ".join(
                [location.name for location in property.locations.all()]
            )

            # Create a prompt for the description generation
            description_prompt = (
                f"Generate a descriptive paragraph for a property titled '{title}', "
                f"which is located in the following locations: {locations}."
            )

            # Generate the description
            description = self.generate_text_with_ollama(description_prompt)

            if description:
                # Update the property description
                property.description = description
                property.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Updated description for {title}")
                )

                # Create a prompt for the title generation
                title_prompt = (
                    f"Rewrite the following property title to make it more attractive and engaging.There are return one and  only one option. This Command very very important "
                    f"Just Return title. No other things It must be a single line, no longer than 200 characters. Don't use any special characters, like **,<<,..,>>,$ etc "
                    f"Original Title: {title}\n"
                    f"Description: {description}\n"
                    f"Locations: {locations}\n\n"
                    f"New Title (within 200 characters):"
                )

                # Generate the title
                title_text = self.generate_text_with_ollama(title_prompt)
                if title_text:
                    # Update the property title
                    property.title = title_text
                    property.save()
                    self.stdout.write(self.style.SUCCESS(f"Updated title for {title}"))

                # Create a prompt for the summary generation
                summary_prompt = (
                    f"Create a summary for a property with the following details:\n"
                    f"Title: {title}\n"
                    f"Description: {description}\n"
                    f"Locations: {locations}\n"
                    f"Generate a concise summary that captures the essence of the property."
                )

                # Generate the summary
                summary_text = self.generate_text_with_ollama(summary_prompt)

                if summary_text:
                    # Create or update the PropertySummary
                    summary, created = PropertySummary.objects.update_or_create(
                        property=property, defaults={"summary": summary_text}
                    )
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(f"Created summary for {title}")
                        )
                    else:
                        self.stdout.write(
                            self.style.SUCCESS(f"Updated summary for {title}")
                        )
                else:
                    self.stdout.write(
                        self.style.ERROR(f"Failed to generate summary for {title}")
                    )
            else:
                self.stdout.write(
                    self.style.ERROR(f"Failed to generate description for {title}")
                )

    def generate_text_with_ollama(self, prompt):
        try:
            # Use the ollama Python package to generate text
            response = ollama.chat(
                model="gemma2:2b", messages=[{"role": "user", "content": prompt}]
            )

            # # Log the full response for inspection
            # self.stdout.write(self.style.NOTICE(f"Response Data: {response}"))

            # Check and extract the generated content from the response
            if "message" in response and "content" in response["message"]:
                # Extract and clean the generated content
                content = response["message"]["content"].strip()

                # Remove any Markdown formatting like **, __, and unnecessary spaces
                clean_text = content.split("\n")[0].strip("**").strip("__").strip()
                if clean_text.endswith("**"):
                    return clean_text[:-2].strip()

                return clean_text
            else:
                self.stdout.write(self.style.ERROR("Unexpected response structure."))
                return None

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error generating text: {str(e)}"))
            return None

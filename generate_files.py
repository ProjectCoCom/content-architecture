import re
import os

def parse_source_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Split the content into sections based on the "---" separator
    sections = content.split('\n---\n')

    parsed_sections = []
    for section_content in sections:
        # Find the main heading of the section
        match = re.search(r'## (\d+)\. (.+)', section_content)
        if match:
            section_number = int(match.group(1))
            title = match.group(2).strip()

            parsed_sections.append({
                'number': section_number,
                'title': title,
                'content': section_content
            })

    return parsed_sections

def clean_content(content):
    """Removes all HTML comments from the content."""
    return re.sub(r'<!-- .*? -->', '', content, flags=re.DOTALL)

def get_blueprint_content(section_content):
    # Tier shared content
    tier_shared_match = re.search(r'<!-- TIER_SHARED_START -->(.*?)<!-- TIER_SHARED_END -->', section_content, re.DOTALL)
    tier_shared_content = tier_shared_match.group(1).strip() if tier_shared_match else ''

    # Blueprint action content
    blueprint_action_match = re.search(r'<!-- BLUEPRINT_ACTION_START -->(.*?)<!-- BLUEPRINT_ACTION_END -->', section_content, re.DOTALL)
    blueprint_action_content = blueprint_action_match.group(1).strip() if blueprint_action_match else ''

    # Extract What This Is and Why This Matters
    what_this_is_match = re.search(r'### What This Is\n(.*?)\n### Why This Matters', section_content, re.DOTALL)
    what_this_is_content = what_this_is_match.group(1).strip() if what_this_is_match else ''

    why_this_matters_match = re.search(r'### Why This Matters\n(.*?)(?=\n###)', section_content, re.DOTALL)
    why_this_matters_content = why_this_matters_match.group(1).strip() if why_this_matters_match else ''

    full_content = f"### What This Is\n{what_this_is_content}\n\n### Why This Matters\n{why_this_matters_content}\n\n{blueprint_action_content}"
    return clean_content(full_content)

def get_system_content(section_content):
    # Tier shared content
    tier_shared_match = re.search(r'<!-- TIER_SHARED_START -->(.*?)<!-- TIER_SHARED_END -->', section_content, re.DOTALL)
    tier_shared_content = tier_shared_match.group(1).strip() if tier_shared_match else ''

    # System only content
    system_only_match = re.search(r'<!-- SYSTEM_ONLY_START -->(.*?)<!-- SYSTEM_ONLY_END -->', section_content, re.DOTALL)
    system_only_content = system_only_match.group(1).strip() if system_only_match else ''

    # System action content
    system_action_match = re.search(r'<!-- SYSTEM_ACTION_START -->(.*?)<!-- SYSTEM_ACTION_END -->', section_content, re.DOTALL)
    system_action_content = system_action_match.group(1).strip() if system_action_match else ''

    # System shared content
    system_shared_match = re.search(r'<!-- SYSTEM_SHARED_START -->(.*?)<!-- SYSTEM_SHARED_END -->', section_content, re.DOTALL)
    system_shared_content = system_shared_match.group(1).strip() if system_shared_match else ''

    # Extract What This Is and Why This Matters
    what_this_is_match = re.search(r'### What This Is\n(.*?)\n### Why This Matters', section_content, re.DOTALL)
    what_this_is_content = what_this_is_match.group(1).strip() if what_this_is_match else ''

    why_this_matters_match = re.search(r'### Why This Matters\n(.*?)(?=\n###)', section_content, re.DOTALL)
    why_this_matters_content = why_this_matters_match.group(1).strip() if why_this_matters_match else ''

    full_content = f"### What This Is\n{what_this_is_content}\n\n### Why This Matters\n{why_this_matters_content}\n\n{tier_shared_content}\n\n{system_only_content}\n\n{system_action_content}\n\n{system_shared_content}"
    return clean_content(full_content)

def get_toolkit_content(section_content):
    # Tier shared content
    tier_shared_matches = re.findall(r'<!-- TIER_SHARED_START -->(.*?)<!-- TIER_SHARED_END -->', section_content, re.DOTALL)
    tier_shared_content = "\n".join(match.strip() for match in tier_shared_matches)

    # System only content
    system_only_matches = re.findall(r'<!-- SYSTEM_ONLY_START -->(.*?)<!-- SYSTEM_ONLY_END -->', section_content, re.DOTALL)
    system_only_content = "\n".join(match.strip() for match in system_only_matches)

    # Toolkit only content
    toolkit_only_matches = re.findall(r'<!-- TOOLKIT_ONLY_START -->(.*?)<!-- TOOLKIT_ONLY_END -->', section_content, re.DOTALL)
    toolkit_only_content = "\n".join(match.strip() for match in toolkit_only_matches)

    # Toolkit action content
    toolkit_action_match = re.search(r'<!-- TOOLKIT_ACTION_START -->(.*?)<!-- TOOLKIT_ACTION_END -->', section_content, re.DOTALL)
    toolkit_action_content = toolkit_action_match.group(1).strip() if toolkit_action_match else ''

    # System shared content
    system_shared_matches = re.findall(r'<!-- SYSTEM_SHARED_START -->(.*?)<!-- SYSTEM_SHARED_END -->', section_content, re.DOTALL)
    system_shared_content = "\n".join(match.strip() for match in system_shared_matches)

    # Extract What This Is and Why This Matters
    what_this_is_match = re.search(r'### What This Is\n(.*?)\n### Why This Matters', section_content, re.DOTALL)
    what_this_is_content = what_this_is_match.group(1).strip() if what_this_is_match else ''

    why_this_matters_match = re.search(r'### Why This Matters\n(.*?)(?=\n###)', section_content, re.DOTALL)
    why_this_matters_content = why_this_matters_match.group(1).strip() if why_this_matters_match else ''

    full_content = f"### What This Is\n{what_this_is_content}\n\n### Why This Matters\n{why_this_matters_content}\n\n{tier_shared_content}\n\n{system_only_content}\n\n{toolkit_only_content}\n\n{toolkit_action_content}\n\n{system_shared_content}"
    return clean_content(full_content)

def generate_files(sections):
    base_path = "The_Ultimate_Content_Architecture_System"
    tiers = ["Blueprint", "System", "Toolkit"]

    for section in sections:
        number = section['number']
        title = section['title']
        content = section['content']

        # Sanitize title for filename
        filename_title = title.lower().replace(' ', '-').replace('&', 'and').replace('.', '')
        filename = f"{number:02d}-{filename_title}.md"

        # Generate content for each tier
        blueprint_content = get_blueprint_content(content)
        system_content = get_system_content(content)
        toolkit_content = get_toolkit_content(content)

        tier_contents = {
            "Blueprint": blueprint_content,
            "System": system_content,
            "Toolkit": toolkit_content
        }

        for tier in tiers:
            filepath = os.path.join(base_path, tier, filename)

            with open(filepath, 'w') as f:
                f.write(f"# {title}\n\n{tier_contents[tier]}")
            print(f"Generated {filepath}")

if __name__ == "__main__":
    sections = parse_source_file("The_Ultimate_Content_Architecture_System/source.md")
    generate_files(sections)
    print("All files generated successfully.")

import re
import os

def parse_source_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Use a positive lookahead to split the content by section headers, keeping the headers.
    # This is more robust than splitting by '---'.
    sections = re.split(r'(?=\n## \d+\. )', content)

    # The first element of the split is the content before the first section header, so we skip it.
    section_contents = sections[1:]

    parsed_sections = []
    for section_content in section_contents:
        # Find the main heading of the section
        match = re.search(r'## (\d+)\. (.+)', section_content)
        if match:
            section_number = int(match.group(1))
            title = match.group(2).strip()

            parsed_sections.append({
                'number': section_number,
                'title': title,
                'content': section_content.strip()
            })

    return parsed_sections

def clean_content(content):
    """Removes all HTML comments from the content."""
    return re.sub(r'<!-- .*? -->', '', content, flags=re.DOTALL)

def get_blueprint_content(section_content):
    # Tier shared content
    tier_shared_match = re.search(r'<!-- TIER_SHARED_START -->(.*?)<!-- TIER_SHARED_END -->', section_content, re.DOTALL)
    tier_shared_content = tier_shared_match.group(1).strip() if tier_shared_match else ''

    # Blueprint only content
    blueprint_only_match = re.search(r'<!-- BLUEPRINT_ONLY_START -->(.*?)<!-- BLUEPRINT_ONLY_END -->', section_content, re.DOTALL)
    blueprint_only_content = blueprint_only_match.group(1).strip() if blueprint_only_match else ''

    # Blueprint action content
    blueprint_action_match = re.search(r'<!-- BLUEPRINT_ACTION_START -->(.*?)<!-- BLUEPRINT_ACTION_END -->', section_content, re.DOTALL)
    blueprint_action_content = blueprint_action_match.group(1).strip() if blueprint_action_match else ''

    # Extract What This Is and Why This Matters
    what_this_is_match = re.search(r'### What This Is\n(.*?)\n### Why This Matters', section_content, re.DOTALL)
    what_this_is_content = what_this_is_match.group(1).strip() if what_this_is_match else ''

    why_this_matters_match = re.search(r'### Why This Matters\n(.*?)(?=\n###|\n<!--)', section_content, re.DOTALL)
    why_this_matters_content = why_this_matters_match.group(1).strip() if why_this_matters_match else ''

    full_content = f"### What This Is\n{what_this_is_content}\n\n### Why This Matters\n{why_this_matters_content}\n\n{blueprint_only_content}\n\n{blueprint_action_content}"
    return clean_content(full_content)

def get_system_content(section_content, include_action_steps=True):
    # Tier shared content
    tier_shared_match = re.search(r'<!-- TIER_SHARED_START -->(.*?)<!-- TIER_SHARED_END -->', section_content, re.DOTALL)
    tier_shared_content = tier_shared_match.group(1).strip() if tier_shared_match else ''

    # System only content
    system_only_matches = re.findall(r'<!-- SYSTEM_ONLY_START -->(.*?)<!-- SYSTEM_ONLY_END -->', section_content, re.DOTALL)
    system_only_content = "\n".join(match.strip() for match in system_only_matches)

    # System action content
    system_action_match = re.search(r'<!-- SYSTEM_ACTION_START -->(.*?)<!-- SYSTEM_ACTION_END -->', section_content, re.DOTALL)
    system_action_content = system_action_match.group(1).strip() if system_action_match else ''

    # System shared content
    system_shared_match = re.search(r'<!-- SYSTEM_SHARED_START -->(.*?)<!-- SYSTEM_SHARED_END -->', section_content, re.DOTALL)
    system_shared_content = system_shared_match.group(1).strip() if system_shared_match else ''

    # Extract What This Is and Why This Matters
    what_this_is_match = re.search(r'### What This Is\n(.*?)\n### Why This Matters', section_content, re.DOTALL)
    what_this_is_content = what_this_is_match.group(1).strip() if what_this_is_match else ''

    why_this_matters_match = re.search(r'### Why This Matters\n(.*?)(?=\n###|\n<!--)', section_content, re.DOTALL)
    why_this_matters_content = why_this_matters_match.group(1).strip() if why_this_matters_match else ''

    parts = [
        f"### What This Is\n{what_this_is_content}",
        f"### Why This Matters\n{why_this_matters_content}",
        tier_shared_content,
        system_only_content,
    ]
    if include_action_steps and system_action_content:
        parts.append(system_action_content)
    if system_shared_content:
        parts.append(system_shared_content)

    full_content = "\n\n".join(part for part in parts if part)
    return clean_content(full_content)

def get_toolkit_content(section_content):
    system_content_base = get_system_content(section_content, include_action_steps=False)

    # Toolkit only content
    toolkit_only_matches = re.findall(r'<!-- TOOLKIT_ONLY_START -->(.*?)<!-- TOOLKIT_ONLY_END -->', section_content, re.DOTALL)
    toolkit_only_content = "\n".join(match.strip() for match in toolkit_only_matches)

    # Toolkit action content
    toolkit_action_match = re.search(r'<!-- TOOLKIT_ACTION_START -->(.*?)<!-- TOOLKIT_ACTION_END -->', section_content, re.DOTALL)
    toolkit_action_content = toolkit_action_match.group(1).strip() if toolkit_action_match else ''

    parts = [
        system_content_base,
        toolkit_only_content,
        toolkit_action_content,
    ]

    full_content = "\n\n".join(part for part in parts if part)
    return clean_content(full_content)

def generate_files(sections):
    base_path = "The_Ultimate_Content_Architecture_System"
    tiers = ["1_Blueprint", "2_System", "3_Toolkit"]

    # Create tier directories if they don't exist
    for tier in tiers:
        os.makedirs(os.path.join(base_path, tier), exist_ok=True)

    if len(sections) != 24:
        print(f"Error: Expected 24 sections, but found {len(sections)}.")
        # We don't return here anymore, to see what it generates.
        # return

    for section in sections:
        number = section['number']
        title = section['title']
        content = section['content']

        # Sanitize title for filename
        filename_title = title.lower().replace(' ', '_').replace('&', 'and').replace('.', '')
        filename = f"{number:02d}_{filename_title}.md"

        # Generate content for each tier
        blueprint_content = get_blueprint_content(content)
        system_content = get_system_content(content)
        toolkit_content = get_toolkit_content(content)

        tier_contents = {
            "1_Blueprint": blueprint_content,
            "2_System": system_content,
            "3_Toolkit": toolkit_content
        }

        for tier in tiers:
            filepath = os.path.join(base_path, tier, filename)

            # Prepend the main title to the content
            final_content = f"# {title}\n\n{tier_contents[tier]}\n"

            with open(filepath, 'w') as f:
                f.write(final_content)
            print(f"Generated {filepath}")

if __name__ == "__main__":
    sections = parse_source_file("The_Ultimate_Content_Architecture_System/source.md")
    generate_files(sections)
    print("All files generated successfully.")

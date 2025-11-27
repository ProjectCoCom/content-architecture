# The Ultimate Content Architecture System

Welcome to The Ultimate Content Architecture System, a comprehensive, tiered framework designed to help you build a powerful, scalable, and effective content strategy. This system is sold as a digital product with three distinct tiers, each tailored to a different level of required guidance and support.

## Three Tiers of Guidance

This system is structured into three tiers, allowing you to choose the level of detail and support that best fits your needs.

### 1. The Blueprint Tier (`/Blueprint`)

The **Blueprint** tier provides the foundational framework of the content architecture system. It's designed for those who need a clear roadmap and are comfortable with high-level strategic concepts.

*   **What's Included**: A comprehensive ebook, access to the private Facebook community, and free lifetime updates.
*   **Who It's For**: Experienced content strategists, seasoned marketers, or anyone who wants a strong strategic foundation without extensive hand-holding.

### 2. The System Tier (`/System`)

The **System** tier offers a much more detailed and descriptive guide to implementing the content architecture. It's designed for users who want a thorough, step-by-step process to follow.

*   **What's Included**: The complete ebook and a detailed digital workbook, plus access to the private Facebook group, an exclusive Substack newsletter, and free lifetime updates.
*   **Who It's For**: In-house marketing teams, content managers, and solopreneurs who want a clear, repeatable system to execute.

### 3. The Toolkit Tier (`/Toolkit`)

The **Toolkit** tier is the complete, "full hand-holding" package. It provides not just the strategy and the system, but all the tools and assets you need to execute with precision and efficiency.

*   **What's Included**: The ebook, workbook, Facebook group and Substack access, plus a complete set of interactive templates, downloadable spreadsheets, online tools, video walkthroughs for each module, and free lifetime updates.
*   **Who It's For**: Marketing agencies, consultants, and teams who need a complete, turnkey solution for executing a sophisticated content strategy for themselves or their clients.

## Content Management

All content for the three tiers is generated from a single source of truth: the `source.md` file. This file uses special comment tags to delineate which content belongs to which tier.

### How to Update Content

To update the content for any of the tiers, follow these steps:

1.  **Edit the `source.md` file:** Make your changes directly in the `source.md` file. Use the existing comment tags (`<!-- TIER_SHARED_START -->`, `<!-- SYSTEM_ONLY_START -->`, etc.) to specify which tiers your content should appear in.
2.  **Run the generation script:** Once you have saved your changes to `source.md`, run the following command from the root of the repository to regenerate all the deliverable files:

    ```bash
    python3 generate_files.py
    ```

This will update all 72 markdown files in the `1_Blueprint`, `2_System`, and `3_Toolkit` directories with your changes.

V0.1 
- python cli.py build sample.epub --out ./build



1. Finalize the content/blocks pipeline

Ensure all block types (text, images, maybe tables/figures) are handled consistently.

Confirm token counts are accurate if you plan to do segmentation or AI-related processing.

Optional: add metadata like page number, chapter, heading level for richer blocks.

2. Rendering / reader integration

Build a simple HTML/JS reader that consumes the generated JSON blocks and renders text + images.

Ensure images referenced in JSON (resources_uri) are correctly loaded relative to the HTML.

Optional: support image zoom, lazy loading, and navigation between blocks/segments.

3. Segmentation & navigation

Use segments.py to break content into manageable chunks (for example, for AI consumption or streaming).

Map blocks → segments → chapters, so your reader or downstream processes can easily paginate or index content.

4. Remote hosting / pre-processing

Right now images and resources are local. Later, you can:

Upload images to S3 or another storage.

Replace resources_uri in JSON with the public URL.

This enables server-side hosting without embedding resources.

5. Optional enhancements

Preprocessing pipeline:

Extract images once (copy_images_from_epub).

Generate blocks/segments.

Store JSON in a structured folder per book/chapter.

Metadata enrichment: add chapter titles, headings, or footnotes.

Error handling / logging: e.g., missing images, broken links, unsupported tags.

6. Integration with AI or search

If the eventual goal is indexing for AI queries:

Use segments + token counts to create embeddings or vector representations.

Ensure blocks/segments are self-contained but context-rich.
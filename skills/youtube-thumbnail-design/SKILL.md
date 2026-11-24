---
name: youtube-thumbnail-design
description: Plan and build truthful YouTube thumbnail variants from supplied or licensed local assets, with mobile-size checks and an explicit boundary around optional image-generation providers.
---
# Local-first YouTube Thumbnails

1. Inspect the video promise, intended viewer, supplied assets, existing approved master and output folder. Confirm image/likeness rights. Preserve originals and previous versions; do not invent a face, evidence screenshot or result.
2. Choose one clear visual idea that complements rather than repeats the title. Prepare two or three materially different concepts only when useful. Use strong subject/background separation, readable contrast, generous edges and very few large words. Faces, bright colors and shocked expressions are choices, not guaranteed CTR improvements.
3. Use the destination's existing authorized local image/SVG/browser rendering tools and supplied/licensed assets. Designed text/vector thumbnails do not need a cloud model. Do not run inference.sh/curl-pipe installers or assume a generation API exists. If original image generation is requested, use a separately configured authorized provider, check cost/privacy permissions, and do not start a duplicate queued job. Identity fidelity requires approved source assets and fresh review.
4. Use 16:9 (typically 1280x720 or 1920x1080) for a standard long-form cover; verify current official YouTube size/format limits for the actual upload surface before delivery. Avoid critical detail at edges and duration-overlay corners. Keep content truthful and supported by the video, not fabricated proof.
5. Export versioned PNG/JPEG files under Thumbnails/<project>/ with editable source, asset/rights notes and a 120px-wide preview. Inspect the actual full-size export and small preview for text readability, clear subject, contrast, crop, edge artifacts and likeness. Verify actual dimensions, file format and bytes. A successful renderer exit is not visual approval.
6. Deliver the exact approved variant with its path/attachment; retain alternative concepts separately. Suggest one-variable tests but do not claim measured CTR or a winning variant without real analytics. Uploading or starting a platform A/B test requires separate user-authorized account access.

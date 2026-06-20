import type { Chapter } from "../types";

interface ImageFrameProps {
  chapter: Chapter;
}

export function ImageFrame({ chapter }: ImageFrameProps) {
  return (
    <div className="image-frame">
      <img src={chapter.image_url} alt={chapter.title} />
    </div>
  );
}

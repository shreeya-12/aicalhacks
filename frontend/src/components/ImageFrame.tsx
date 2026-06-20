import { useState, useEffect } from "react";
import type { Chapter } from "../types";

interface ImageFrameProps {
  chapter: Chapter;
}

export function ImageFrame({ chapter }: ImageFrameProps) {
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    setLoaded(false);
  }, [chapter.image_url]);

  return (
    <div className="image-frame">
      <div className="image-wrapper">
        {!loaded && <div className="image-skeleton" />}
        <img
          src={chapter.image_url}
          alt={chapter.title}
          style={{ opacity: loaded ? 1 : 0 }}
          onLoad={() => setLoaded(true)}
        />
      </div>
      <p className="image-caption">{chapter.image_prompt}</p>
    </div>
  );
}

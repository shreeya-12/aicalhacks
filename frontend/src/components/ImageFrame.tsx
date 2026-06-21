import { useState, useEffect, useRef } from "react";
import type { Chapter } from "../types";

interface ImageFrameProps {
  chapter: Chapter;
}

export function ImageFrame({ chapter }: ImageFrameProps) {
  const [loaded, setLoaded] = useState(false);
  const imgRef = useRef<HTMLImageElement>(null);

  useEffect(() => {
    // If the image (often an already-decoded data URI) is complete before the
    // onLoad handler attaches — e.g. navigating away and back — onLoad never
    // fires, so check .complete directly to avoid an infinite skeleton.
    const img = imgRef.current;
    if (img && img.complete && img.naturalWidth > 0) {
      setLoaded(true);
    } else {
      setLoaded(false);
    }
  }, [chapter.image_url]);

  return (
    <div className="image-frame">
      <div className={`image-wrapper${loaded ? " loaded" : ""}`}>
        {!loaded && <div className="image-skeleton" />}
        <img
          ref={imgRef}
          src={chapter.image_url}
          alt={chapter.title}
          style={{ opacity: loaded ? 1 : 0 }}
          onLoad={() => setLoaded(true)}
          onError={() => setLoaded(true)}
        />
      </div>
      <p className="image-caption">{chapter.image_prompt}</p>
    </div>
  );
}

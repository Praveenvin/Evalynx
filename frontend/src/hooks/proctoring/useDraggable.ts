import { useState, useRef, useEffect, MouseEvent as ReactMouseEvent, TouchEvent as ReactTouchEvent } from "react";

export function useDraggable() {
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const isDragging = useRef(false);
  const dragStartPos = useRef({ x: 0, y: 0 });
  const initialPos = useRef({ x: 0, y: 0 });

  const handlePointerDown = (clientX: number, clientY: number) => {
    isDragging.current = true;
    dragStartPos.current = { x: clientX, y: clientY };
    initialPos.current = { ...position };
  };

  const handlePointerMove = (clientX: number, clientY: number) => {
    if (!isDragging.current) return;
    
    const dx = clientX - dragStartPos.current.x;
    const dy = clientY - dragStartPos.current.y;
    
    // We update position via state, which causes re-render.
    // For smoother perf, we could use a ref + direct DOM manipulation, 
    // but React state is fine for this lightweight overlay.
    setPosition({
      x: initialPos.current.x + dx,
      y: initialPos.current.y + dy
    });
  };

  const handlePointerUp = () => {
    isDragging.current = false;
  };

  useEffect(() => {
    const onMouseMove = (e: MouseEvent) => handlePointerMove(e.clientX, e.clientY);
    const onMouseUp = () => handlePointerUp();
    const onTouchMove = (e: TouchEvent) => handlePointerMove(e.touches[0].clientX, e.touches[0].clientY);
    const onTouchEnd = () => handlePointerUp();

    if (isDragging.current) {
      document.addEventListener("mousemove", onMouseMove);
      document.addEventListener("mouseup", onMouseUp);
      document.addEventListener("touchmove", onTouchMove, { passive: false });
      document.addEventListener("touchend", onTouchEnd);
    }

    return () => {
      document.removeEventListener("mousemove", onMouseMove);
      document.removeEventListener("mouseup", onMouseUp);
      document.removeEventListener("touchmove", onTouchMove);
      document.removeEventListener("touchend", onTouchEnd);
    };
  }); // run on every render so we attach when dragging starts

  const onMouseDown = (e: ReactMouseEvent) => handlePointerDown(e.clientX, e.clientY);
  const onTouchStart = (e: ReactTouchEvent) => handlePointerDown(e.touches[0].clientX, e.touches[0].clientY);

  return {
    position,
    onMouseDown,
    onTouchStart,
  };
}

<script lang="ts">
  import { onMount } from "svelte";

  let ctx: CanvasRenderingContext2D | null = null;

  let isDrawing = false;
  let width = 450;
  let height = 400;

  let topHand = 0;
  let leftHand = 0;

  let start = { x: 0, y: 0 };

  let {
    color,
    background,
    canvas = $bindable(),
  }: {
    color: string;
    background: string;
    canvas: HTMLCanvasElement;
  } = $props();

  const handleSize = () => {
    const { top, left } = canvas.getBoundingClientRect();
    topHand = top;
    leftHand = left;
  };

  onMount(() => {
    ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, width, height);
    ctx.lineWidth = 3;

    canvas.style.borderRadius = "40px";
    handleSize();
  });

  //effect: update stroke when color changes
  $effect(() => {
    if (ctx) ctx.strokeStyle = color;
  });

  const handleStart = ({
    offsetX: x,
    offsetY: y,
  }: {
    offsetX: number;
    offsetY: number;
  }) => {
    if (!ctx) return;

    // “eraser” mode ,clear canvas
    if (color === background) {
      ctx.fillRect(0, 0, width, height);
      return;
    }

    isDrawing = true;
    start = { x, y };
  };

  const handleEnd = () => {
    isDrawing = false;
  };

  const handleMove = ({
    offsetX: x1,
    offsetY: y1,
  }: {
    offsetX: number;
    offsetY: number;
  }) => {
    if (!ctx || !isDrawing) return;

    const { x, y } = start;
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x1, y1);
    ctx.stroke();

    start = { x: x1, y: y1 };
  };
</script>

<svelte:window on:resize={handleSize} />

<canvas
  class="cursor-grabbing"
  {width}
  {height}
  bind:this={canvas}
  onmousedown={handleStart}
  onmouseup={handleEnd}
  onmouseleave={handleEnd}
  onmousemove={handleMove}
  ontouchstart={(e) => {
    const { clientX, clientY } = e.touches[0];
    handleStart({
      offsetX: clientX - leftHand,
      offsetY: clientY - topHand,
    });
  }}
  ontouchend={handleEnd}
  ontouchmove={(e) => {
    const { clientX, clientY } = e.touches[0];
    handleMove({
      offsetX: clientX - leftHand,
      offsetY: clientY - topHand,
    });
  }}
></canvas>

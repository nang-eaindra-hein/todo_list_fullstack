<script lang="ts">
  import Button from "$lib/components/Button.svelte";
  import Canvas from "$lib/components/Canvas.svelte";
  import Palette from "$lib/components/Palette.svelte";
  import { goto } from "$app/navigation";
  import { createMutation, useQueryClient } from "@tanstack/svelte-query";
  import { page } from "$app/stores";
  import { get } from "svelte/store";

  import { toast, Toaster } from "svelte-french-toast";

  import { createDraw } from "$lib/drawApi";

  const colors = [
    "#d58141",
    "#d7c44c",
    "#4fa9cc",
    "#3f8d27",
    "#f2acf0",
    "#97cffc",
    "#63f054",
    "#000000",
    "#ad0a0a",
    "#fdff91",
    "#ffffff",
    "#61ffe7",
    "#c4a178",
    "#b584e3",
    "#b01283",
    "#2712b0",
    "#12b02c",
    "#f28627",
    "#6d7a7a",
    "#242315",
    "#4f4348",
  ];
  const background = "#fff";

  const todoId = Number(get(page).params.todoId);
  const qc = useQueryClient();
  import { getDraw, type Draw } from "$lib/drawApi";

  import { createQuery } from "@tanstack/svelte-query";
  let color = $derived(colors[0]);
  let canvas: HTMLCanvasElement;
  let dataURL = $state("");
  //back btn
  function goBack() {
    if (window.history.length > 1) {
      window.history.back();
    } else {
      goto("/");
    }
  }
  //down canvas
  function downloadCanvas() {
    dataURL = canvas.toDataURL("image/png");
    const link = document.createElement("a");
    link.download = "canvas-image.png";
    link.href = dataURL;
    link.click();
  }

  //add func
  function saveDraw(todoId: number, dataURL: string) {
    if (!canvas) return;
    dataURL = canvas.toDataURL("image/png");
    const img = dataURL.trim();
    if (!img) return;
    createMut.mutate({ todoId, img });
  }
  //get mutation
  const drawQuery = createQuery<Draw[]>(() => ({
    queryKey: ["draw"],
    queryFn: () => getDraw(todoId),
  }));
  function loadToCanvas(dataURL: string) {
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const img = new Image();
    img.onload = () => {
      ctx.drawImage(img, 0, 0, canvas!.width, canvas!.height);
    };
    img.src = dataURL;
  }

  $effect(() => {
    const list = drawQuery.data ?? [];
    const latest = list[list.length - 1];
    if (latest?.img) queueMicrotask(() => loadToCanvas(latest.img));
  });

  // SAVE mutation
  const saveMut = createMutation(() => ({
    mutationFn: async () => {
      if (!canvas) throw new Error("no canvas");
      const dataURL = canvas.toDataURL("image/png");
      return saveDraw(todoId, dataURL);
    },
    onSuccess: async (_saved) => {
      await qc.invalidateQueries({ queryKey: ["draw", todoId] });
      queueMicrotask(() => loadToCanvas(dataURL));
    },
  }));
  //create mutation

  const createMut = createMutation(() => ({
    mutationFn: ({ todoId, img }: { todoId: number; img: string }) =>
      createDraw(todoId, { img }),
    onSuccess: async () => {
      dataURL = "";

      await qc.invalidateQueries({ queryKey: ["draw"] });
    },
  }));
</script>

<h1
  class="text-purple-900 justify-center flex text-2xl pb-5 underline font-bold"
>
  Draw
</h1>

<Button onclick={goBack} variant="Blue">back</Button>

<Button
  variant="Green"
  onclick={() => {
    toast.success("Downloaded Successfully!");
    downloadCanvas;
  }}>Download</Button
>

<Button
  variant="Green"
  onclick={() => {
    saveMut.mutate();
    toast.success("Saved Canvas Successfully!");
  }}>Saved</Button
>
<!--canvas show-->
<div class="h-screen flex justify-center items-center">
  <div class="space-y-5">
    <Canvas {color} {background} bind:canvas />
    <Palette
      paletteColor={color}
      {colors}
      {background}
      on:color={({ detail }) => {
        color = detail.color;
      }}
    />
  </div>
</div>

<Toaster />

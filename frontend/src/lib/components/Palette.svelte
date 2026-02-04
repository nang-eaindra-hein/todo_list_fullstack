<script lang="ts">
  import { createEventDispatcher } from "svelte";
  const dispatch = createEventDispatcher();

  let {
    paletteColor,
    colors,
    background,
  }: { paletteColor: string; colors: string[]; background: string } = $props();
</script>

<div class=" flex justify-between gap-3">
  <div class="gap-2 grid grid-cols-7 grid-rows-2">
    {#each colors as c}
      <button
        type="button"
        onclick={() => dispatch("color", { color: c })}
        style="background:{c}; width:32px; height:32px; border-radius:10px;"
        class={paletteColor === c
          ? "ring-2 ring-black cursor-grabbing"
          : "cursor-grab"}
      >
        <span class="hidden">{c}</span>
      </button>
    {/each}
  </div>
  <div class="flex gap-3">
    <button
      type="button"
      onclick={() => dispatch("color", { color: background })}
      style="background:{background}; width:32px; height:32px; border-radius:10px;"
      class={paletteColor === background
        ? "ring-2 ring-black cursor-grabbing"
        : "cursor-grab"}
    >
      <span class="text-xs">clear</span>
    </button>

    <svg style:color={paletteColor} viewBox="-50 -50 100 100" class="w-10 h-10">
      <g
        fill="currentColor"
        stroke="currentColor"
        stroke-width="0"
        stroke-linecap="round"
      >
        <path d="M -38 12 a 38 38 0 0 0 76 0 q 0 -28 -38 -62 -38 34 -38 62" />
      </g>
    </svg>
  </div>
</div>

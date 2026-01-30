<script lang="ts">
  import type { Snippet } from "svelte";
  import type { HTMLButtonAttributes } from "svelte/elements";

  let {
    onclick,
    disabled,
    children,
    variant = "Blue",
  }: {
    onclick?: (e: MouseEvent) => void;

    disabled?: Boolean;
    children?: Snippet;
    variant?: "Green" | "Blue" | "Red";
  } & HTMLButtonAttributes = $props();
</script>

<button
  {onclick}
  {disabled}
  class="rounded-md px-2 cursor-pointer {variant == 'Green'
    ? 'bg-green-200'
    : variant == 'Red'
      ? 'bg-red-200'
      : variant == 'Blue'
        ? 'bg-blue-200'
        : ''}"
>
  <span> {@render children?.()}</span>
</button>

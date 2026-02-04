<script lang="ts">
  import { onMount } from "svelte";
  import Button from "./Button.svelte";
  let isDark = $state(false);

  onMount(() => {
    const saved = localStorage.getItem("isDark");
    const systemDark = window.matchMedia(
      "(prefer-colour-scheme:'dark')"
    ).matches;
    isDark = saved === null ? systemDark : saved === "true";
    document.documentElement.classList.toggle("dark", isDark);
  });

  function toggleDark() {
    isDark = !isDark;
    document.documentElement.classList.toggle("dark", isDark);
    localStorage.setItem("isDark", String(isDark));
  }
</script>

<Button onclick={toggleDark} variant="Blue">
  {#if isDark}
    <div>Light Mode</div>
  {:else}
    <div>Dark Mode</div>
  {/if}
</Button>

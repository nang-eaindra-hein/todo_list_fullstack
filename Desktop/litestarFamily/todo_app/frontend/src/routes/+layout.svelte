<script lang="ts">
  import "./layout.css";
  import { QueryClient } from "@tanstack/svelte-query";
  import { QueryClientProvider } from "@tanstack/svelte-query";
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        refetchOnWindowFocus: false,
      },
    },
  });

  let { children } = $props();
</script>

<QueryClientProvider client={queryClient}>
  {@render children()}
</QueryClientProvider>

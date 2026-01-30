<script lang="ts">
  import {
    createQuery,
    createMutation,
    useQueryClient,
  } from "@tanstack/svelte-query";

  import {
    getTodos,
    checkboxTodo,
    updateTodo,
    deleteTodo,
    createTodo,
    type Todo,
  } from "$lib/todoApi";
  import Lists from "$lib/components/Lists.svelte";
  import Button from "$lib/components/Button.svelte";

  const qc = useQueryClient();

  let filter = $state<"filter" | "all" | "active" | "done">("filter");
  let newTitle = $state("");
  const statusParam = $derived(
    filter === "filter" ? undefined : filter === "done"
  );
  //add func
  function add() {
    const title = newTitle.trim();
    if (!title) return;
    createMut.mutate(title);
  }
  //get mutation
  const todosQuery = createQuery<Todo[]>(() => ({
    queryKey: ["todos", filter],
    queryFn: () => getTodos(statusParam),
  }));

  //create mutation

  const createMut = createMutation(() => ({
    mutationFn: (title: string) => createTodo({ title, status: false }),
    onSuccess: async () => {
      newTitle = "";
      await qc.invalidateQueries({ queryKey: ["todos"] });
    },
  }));
</script>

<div class=" bg-amber-100 h-screen">
  <div class="flex pb-5 justify-center text-xl font-bold items-center">
    Todo List
  </div>
  <!--refresh-->
  <Button
    variant="Blue"
    onclick={() => todosQuery.refetch()}
    disabled={todosQuery.isFetching}
  >
    {todosQuery.isFetching ? "Refreshing..." : "Refresh"}
  </Button>

  <!--create-->
  <div class="flex gap-2 justify-center items-center">
    <div>Create a list</div>
    <input
      class="flex p-2 rounded-lg border"
      placeholder="New todo..."
      bind:value={newTitle}
      onkeydown={(e) => e.key === "Enter" && add()}
    />
    <Button variant="Green" onclick={add} disabled={createMut.isPending}>
      {createMut.isPending ? "Adding..." : "Add"}
    </Button>
  </div>

  <!--dropdown filter-->
  <select class="border rounded-md m-5">
    <div class="flex gap-2">
      <option
        class="cursor-not-allowed"
        onclick={() => (filter = "filter")}
        disabled={filter === "filter"}
      >
        filter
      </option>
      <option
        class="cursor-pointer"
        onclick={() => (filter = "all")}
        disabled={filter === "all"}>All</option
      >

      <option
        class="cursor-pointer"
        onclick={() => (filter = "active")}
        disabled={filter === "active"}>Active</option
      >
      <option
        class="cursor-pointer"
        onclick={() => (filter = "done")}
        disabled={filter === "done"}>Done</option
      >
    </div>
  </select>

  <!--lists-->
  <Lists {qc} {todosQuery} />
</div>

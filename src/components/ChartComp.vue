<script>
export default {
  props: {
    title: String,
  },
};
</script>

<template>
  <div class="bg-white bg-opacity-75 block w-full h-64 rounded-3xl">
    <h1 class="font-bold m-5">{{ title }}</h1>

    <slot></slot>
  </div>
</template>

<template>
  <ul class="tag-list">
    <li v-for="(s,i) in tags" :key="i" v-bind:class="s.type">
      <span v-text="s.text"></span>
      <span v-bind:tag-index="i" v-on:click="onDeleteClicked"></span>
    </li>
  </ul>
</template>
<script>
  import {EventBus} from './EventBus.js'
  export default {
    data () {
      return {

      }
    },
    props: ['tags'],
    methods: {
      onDeleteClicked: function (e) {
        EventBus.$emit('tag-deleted-clicked', e.currentTarget)
      }
    }
  }
</script>

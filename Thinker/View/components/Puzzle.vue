<template>
  <transition-group name="cell" tag="div" class="container">
    <div
      v-for="cell in cells"
      :key="cell.id"
      :class="{
        cell: true,
        click: isClickable(cell.id) && available,
        disable: !available,
        green: green,
        red : red
      }"
      :id="`cell-${cell.id}`"
      @click="move(cell.id)"
      :style="cell.distance == 0 ? `color:var(--oc-green-3)` :`color:var(--oc-cyan-${cell.distance + 2})`"
    >{{ cell.number != 0 ? cell.number : "" }}</div>
  </transition-group>
</template>

<script>
export default {
  props: {
    cells: {
      type: Array,
      required: true
    },
    available: {
      type: Boolean,
      default: true
    },
    green: {
      type: Boolean,
      default: false
    },
    red: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      left: -1,
      right: -1,
      up: -1,
      down: -1
    };
  },
  methods: {
    isClickable(number) {
      if (number == this.left) return true;
      if (number == this.right) return true;
      if (number == this.up) return true;
      if (number == this.down) return true;
      return false;
    },
    move(e) {
      if (!this.available) return;
      if (e == this.left) this.$emit("move", "Right");
      else if (e == this.right) this.$emit("move", "Left");
      else if (e == this.up) this.$emit("move", "Down");
      else if (e == this.down) this.$emit("move", "Up");
    }
  },
  watch: {
    cells(e) {
      let index = this.cells.map(cell => cell.id).indexOf(0);
      this.left = index % 4 < 3 ? this.cells[index + 1].id : -1;
      this.right = 0 < index % 4 ? this.cells[index - 1].id : -1;
      this.up = index / 4 < 3 ? this.cells[index + 4].id : -1;
      this.down = 1 <= index / 4 ? this.cells[index - 4].id : -1;
    }
  }
};
</script>

<style scoped>
.green {
  background: var(--oc-green-1) !important;
  color: black !important;
}
.red {
  background: var(--oc-red-5) !important;
  color: black !important;
}
.disable {
  background: var(--oc-orange-0);
}
.click {
  background: #e6fcf5;
  cursor: pointer;
}
#cell-0 {
  border: none;
  color: transparent;
}
.container {
  display: flex;
  flex-wrap: wrap;
  width: 400px;
  min-height: 0;
  margin: auto;
}
.cell {
  transition: linear 1s;
  font-size: 30px;
  font-weight: 400;
  display: flex;
  justify-content: space-around;
  align-items: center;
  width: 100px;
  height: 100px;
  border: 1px solid #aaa;
}
.cell:nth-child(3n) {
  margin-right: 0;
}
.cell:nth-child(27n) {
  margin-bottom: 0;
}
.cell-move {
  transition: transform 1s;
}
</style>

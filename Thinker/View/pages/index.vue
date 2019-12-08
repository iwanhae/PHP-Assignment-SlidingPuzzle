<template>
  <section class="container">
    <div>
      <h1 class="title">
        <div style="display:flex;margin:auto;">
          AI
          <div style="font-size:30pt;margin: 40px 10px 0px;">assisted</div>Puzzle
        </div>
      </h1>

      <h2 class="subtitle">Internet Programming project</h2>

      <div class="links" style="margin-top:50px;">
        <div class="button--green" @click="shuffle">Shuffle</div>
        <div v-if="available" class="button--green" @click="start">Start</div>
        <div v-if="!available" class="button--green" @click="stop">Stop</div>
      </div>
      <h2 class="subtitle">
        you helped
        <div>{{ counter }}</div>times
      </h2>
      <Puzzle
        :cells="this.cells"
        :available="available"
        :green="Finished"
        :red="red"
        @move="handleMove"
      />

      <h3 class="subtitle">Steps: {{ stepCounter }}</h3>
      <div style="margin:100px"></div>
    </div>
  </section>
</template>

<script>
import AppLogo from "~/components/AppLogo.vue";
import Puzzle from "~/components/Puzzle.vue";
import Axios from "axios";

const one2Two = arr => {
  let output = [];
  for (let i = 0; i < 4; i++) {
    let tmp = [];
    for (let j = 0; j < 4; j++) tmp.push(arr[i * 4 + j]);
    output.push(tmp);
  }
  return output;
};
const two2One = arr => {
  return [].concat(...arr);
};

function distance(cur, dest) {
  const cx = cur % 4;
  const cy = Math.floor(cur / 4);
  const dx = dest % 4;
  const dy = Math.floor(dest / 4);
  return Math.abs(dx - cx) + Math.abs(dy - cy);
}
export default {
  components: {
    AppLogo,
    Puzzle
  },
  methods: {
    async Request(action = "None") {
      let d = await Axios.post("/php/move.php", {
        state: this.state,
        action: action,
        error: false
      });
      return d.data;
    },
    async handleMove(action) {
      this.available = false;
      console.log(action);
      this.counter += 1;

      let data = await this.Request(action);
      this.state = data.state;
      this.syncState();
      this.stepCounter += 1;
      this.available = true;
    },
    shuffle(e) {
      this.counter = 0;
      this.stepCounter = 0;
      this.available = false;
      this.AIturn = false;
      Axios.get("/php/init.php").then(res => {
        console.log(res);
        this.state = res.data;
        this.syncState();
        this.available = true;
      });
    },
    stop(e) {
      this.available = true;
      this.AIturn = false;
    },
    start(e) {
      this.AIturn = true;
      this.AIstep();
    },
    async AIstep(isAuto = false) {
      this.available = false;
      this.AIturn = true;
      if (this.Finished) {
        this.AIturn = false;
        return;
      }
      let data = await this.Request("None");
      this.available = true;
      console.log(data.error);
      if (data.error || !this.AIturn) {
        this.AIturn = false;
        this.red = true;
        setTimeout(() => {
          this.red = false;
        }, 400);
        return;
      } else {
        this.state = data.state;
        this.syncState();
        this.stepCounter += 1;
        this.AIstep(true);
      }
    },
    syncState() {
      let tmp = two2One(this.state).map(function(val, index) {
        return { id: val, number: val, distance: distance(val, index) };
      });
      for (let i = 0; i < 16; i++) {
        if (tmp[i].id == i) this.Finished = true;
        else {
          this.Finished = false;
          break;
        }
      }
      console.log(tmp);
      for (let i = 0; i < this.cells.length; i++)
        this.$set(this.cells, i, tmp[i]);
    },
    async test(e) {
      try {
        let d = await Axios.post("/api", {
          state: this.state
        });
        d = d.data;
        const action = d.action;
        console.log(d);
      } catch {}
    }
  },
  data() {
    return {
      state: [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]],
      cells: Array.apply(null, { length: 16 }).map(function(_, index) {
        return { id: index, number: index };
      }),
      available: true,
      counter: 0,
      stepCounter: 0,
      red: false,
      AIturn: false,
      Finished: false
    };
  },
  mounted() {
    this.shuffle();
  }
};
</script>

<style>
.container {
  min-height: 50vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.title {
  font-family: "Quicksand", "Source Sans Pro", -apple-system, BlinkMacSystemFont,
    "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; /* 1 */
  display: flex;
  font-weight: 300;
  font-size: 80px;
  color: #35495e;
  letter-spacing: 1px;
}

.subtitle {
  font-weight: 300;
  font-size: 42px;
  color: #526488;
  word-spacing: 5px;
  padding-bottom: 15px;
}

.links {
  padding-top: 15px;
}
</style>

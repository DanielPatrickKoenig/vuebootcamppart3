<template>
  <div id="app">
    <div class='main-header'>VUE JS BOOT CAMP</div>
    <div class="charts">
      <barChart :chartdata="comparisondata" :colors="chartColors" :textcolor="chartTextColor" title="Regional Sales"></barChart>
      <pieChart :chartdata="salesdata" :colors="chartColors" :textcolor="chartTextColor" title="Genres" hovertitle='Global Sales'></pieChart>
      <div class="rating-charts">
        <label class="ratings-title" v-text="Object.keys(ratings).length === 0 ? '' : 'Critic Ratings'"></label>
        <ratingChart v-for="(r, k, i) in ratings" :key="i" v-bind:chartdata="r.Critic_Score !== undefined ? r.Critic_Score : 0" v-bind:color="chartColors[0]" v-bind:text="k" v-bind:total="100"></ratingChart>
      </div>
    </div>
    <uiDrawer>
      <span slot="titletext">FILTERS</span>
      <div slot="userinterface">
        <checkAll :choices="checkChoices"></checkAll>
        <searchText :choices="checkChoices" :list="searchableContentFiltered" :exclusions="getExcludeList(selectedTags)"></searchText>
        <tagList :tags="selectedTags"></tagList>
      </div>
    </uiDrawer>
  </div>
</template>

<script>
import {EventBus} from './EventBus.js'
import PiehartComponent from './PieChartComponent.vue'
import BarhartComponent from './BarChartComponent.vue'
import RatingChartComponent from './RatingChartComponent.vue'
import uiDrawerComponent from './UIDrawerComponent.vue'
import CheckAllComponent from './CheckAllComponent.vue'
import SearchTextComponent from './SearchTextComponent.vue'
import TagListComponent from './TagListComponent.vue'
import axios from 'axios'
export default {
  name: 'app',
  components: {
    pieChart: PiehartComponent,
    barChart: BarhartComponent,
    ratingChart: RatingChartComponent,
    uiDrawer: uiDrawerComponent,
    checkAll: CheckAllComponent,
    searchText: SearchTextComponent,
    tagList: TagListComponent
  },
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      chartColors: ['#00aeef', '#fdc689', '#7cc576', '#f26d7d', '#a186be', '#ec008c', '#c69c6d', '#ed145b', '#f26522', '#acd373', '#aba000', '#f5989d'],
      chartTextColor: '#eeeeee',
      checkChoices: [
        {text: 'Genres', value: 'genre', selected: true},
        {text: 'Systems', value: 'system', selected: true},
        {text: 'Publishers', value: 'publisher', selected: true},
        {text: 'Games', value: 'game', selected: true}
      ],
      searchableContent: {},
      searchableContentFiltered: {},
      searchExclusions: [],
      selectedTags: [],
      salesdata: {},
      yeardata: {},
      comparisondata: {},
      ratings: {},
      onUpdateSim: function (d) {
        var splitter = ':::'
        var _params = {}
        for (var i = 0; i < d.selectedTags.length; i++) {
          if (_params[d.selectedTags[i].type] === undefined) {
            _params[d.selectedTags[i].type] = []
          }
          _params[d.selectedTags[i].type].push(d.selectedTags[i].text)
        }
        var params = {splitter: splitter}
        for (var p in _params) {
          params[p] = _params[p].join(splitter)
        }
        console.log(params)
        axios.get('/update', {params: params}).then(response => {
          var dta = JSON.parse(response.data)
          d.salesdata = dta.sales
          d.yeardata = dta.years
          d.comparisondata = dta.subset
          d.ratings = dta.ratings
          console.log(d.comparisondata)
        })
      }
    }
  },
  methods: {
    getExcludeList: function (el) {
      var outList = []
      for (var i = 0; i < el.length; i++) {
        outList.push(el[i].text)
      }
      return outList
    }
  },
  created () {
    var self = this
    EventBus.$on('check-all-option-checked', (n) => {
      self.$data.searchableContentFiltered = {}
      for (var s in self.$data.searchableContent) {
        var isEnabled = false
        for (var i = 0; i < self.$data.checkChoices.length; i++) {
          if (self.$data.checkChoices[i].value === s && self.$data.checkChoices[i].selected) {
            isEnabled = true
          }
        }
        if (isEnabled) {
          self.$data.searchableContentFiltered[s] = self.$data.searchableContent[s]
        }
      }
    })
    EventBus.$on('search-term-clicked', (n) => {
      self.$data.selectedTags.push({type: n.getAttribute('class'), text: n.innerHTML})
      self.$data.onUpdateSim(self.$data)
    })
    EventBus.$on('tag-deleted-clicked', (n) => {
      self.$data.selectedTags.splice(Number(n.getAttribute('tag-index')), 1)
      self.$data.onUpdateSim(self.$data)
    })

    axios.get('/data').then(response => {
      var dta = JSON.parse(response.data)
      var game = dta.namelist
      var genre = dta.genrelist
      var system = dta.systemlist
      var publisher = dta.publisherlist
      self.$data.searchableContent = {genre: genre, system: system, publisher: publisher, game: game}
      self.$data.searchableContentFiltered = {genre: genre, system: system, publisher: publisher, game: game}

      self.$data.onUpdateSim(self.$data)
    })
  }
}
</script>

<style lang="scss">

$genreColor: #9e0039;
$systemColor: #406618;
$publisherColor: #0054a6;
$gameColor: #8c6239;
$bodyBackground: url('assets/bgImage.png');
$textColor: #ffffff;
$uiBackground: rgba(222,243,226,.9);
$chartTitleTextColor: #eeeeee;
$drawerOpenedHeight: 400px;
$drawerClosedHeight: 40px;
$drawerSpeed:.5s;

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
body {
  background-color: #000000;
  padding: 0;
  margin: 0;
  background-image: $bodyBackground;
  background-position: center;
  background-size: cover;
}
div#main{
  /* max-width:1200px; */
  width:100%;
  /* margin:0 auto; */
    
}
div.search-text,
ul.tag-list{
  float:left;
}
div.search-text{
  max-width:780px;
  width:100%;
  position:relative;
  margin:0 10px;
  z-index:20;
  clear:left;
  margin-top:-5px;
  > input[type='text']{
    display:block;
    width:100%;
    max-width:770px;
    height:30px;
    font-size:28px;
    font-weight:bold;
    border:none;
    border-radius:4px;
    box-shadow: 0 0 4px rgba(0, 0, 0, .3) inset;
    padding:0 5px;
  }
  > ul{
    position:absolute;
    max-height:300px;
    overflow:auto;
    width:100%;
    margin:0;
    padding:0;
    > li{
      color:$textColor;
      padding:4px;
      margin:2px 0;
      font-family:Arial;
      font-weight:bold;
      font-size:12px;
      text-align: left;
    }
  }
}

div.search-text > ul > li,
ul.check-all > li{
  display:block;
    
}

ul.tag-list{
  width:400px;
  > li {
    display:inline;
    float:left;
    padding:1px 8px 3px 8px;
    background-color:#ffff00;
    border-radius:100px;
    margin:2px;
    color:$textColor;

    > span:first-child{
      font-family:Arial;
      font-weight:bold;
      font-size:12px;
    }

    > span:last-child{
      display: inline-block;
      background-color: transparent;
      color: $textColor;
      box-shadow: 0 0 0px 1px #ffffff inset;
      border-radius: 20px;
      width: 15px;
      height: 16px;
      font-size: 10px !important;
      margin-right: -4px;
      margin-top: -1px !important;
      text-align:center;
      cursor:pointer;
    }

    > span:last-child::before{
      content:'\2716';
      text-align: center;
    }
  } 
}

ul.tag-list,
ul.check-all,
div.search-text ul{
  > li.genre{
    background-color:$genreColor;
  }
  > li.system{
    background-color:$systemColor;
  }
  > li.publisher{
    background-color:$publisherColor;
  }
  > li.game{
    background-color:$gameColor;
  }
}

ul.check-all,
ul.tag-list{
    margin:0;
    padding:0;
}


div.pie-chart,
div.line-chart,
div.bar-chart{
  display:inline;
  float:left;
}
div.pie-chart > div{
  width:750px;
  height:500px;
}

div.line-chart > div,
div.bar-chart > div{
  width:1200px;
  height:300px;
  box-shadow: 0 -1px 0 rgba(255,255,255,.2) inset; 
  margin-bottom:4px;
}

div.charts{
  max-width:1200px;
  
  position:relative;
  max-width:1200px;
  width:100%;
  margin:0 auto;
}

div.ui-drawer{
  position: fixed;
  width: 100%;
  bottom: 0;
  left:0;
  background-color:$uiBackground;
  input[type='checkbox']{
    display:none;
  }
  > label.open-toggle{
    width: 100%;
    display: block;
    text-align: center;
    height:30px;
    padding-top:8px;
    background-color:rgba(0,0,0,.2);
    + div{
      margin:0 auto;
      max-width:1200px;
      width:100%;
    }
  }
  > label > span{
    margin:0 10px;
    font-weight:bold;
    font-size:14px;
    font-family:Arial;
  }
}

@keyframes opened {
  from {height: $drawerClosedHeight;}
  to {height: $drawerOpenedHeight;}
}

div.ui-drawer.open{
  height: $drawerOpenedHeight;
  animation-name: opened;
  animation-duration: $drawerSpeed;
  > label::after{
    content:'\21E3';
    font-size:25px;
  }
  > label::before{
    content:'\21E3';
    font-size:25px;
  }
}

@keyframes closed {
  from {height: $drawerOpenedHeight;}
  to {height: $drawerClosedHeight;}
}

div.ui-drawer:not(.open){
  height: $drawerClosedHeight;
  animation-name: closed;
  animation-duration: $drawerSpeed;
  > label::after{
    content:'\21E1';
    font-size:25px;
  }
  > label::before{
    content:'\21E1';
    font-size:25px;
  }
}

ul.check-all{
  width:100%;
  height:40px;
  padding-left:10px;
  > li:first-child{
    border-radius:50px 0 0 50px;
  }
  > li:last-child{
    border-radius:0 50px 50px 0;
  }
  > li{
    float:left;
    margin-top:4px;   
    width:195px; 
    color:$textColor;
    font-family:Arial;
    font-weight:bold;
    text-align:center;
    padding:5px 0;
    box-shadow:0 0 0 1px #ffffff inset;
    input[type='checkbox']{
      display:none;
    }
  }
}

ul.tag-list{
    margin-top:-40px;
    max-height:340px;
    overflow-y:auto;

}

div.rating-charts{
  width:450px;
  display: inline-block;
  text-align: left;
  > div.rating-chart{
    margin: 6px 0;
    border-radius: 0 20px 20px 0;
    overflow: hidden;
    width: 100%;
    height: 30px;
    background-color: #cccccc;
    span{
      display:block;
      padding:9px;
      font-family:Arial;
      font-size:11px;
    }
  }
}

label.ratings-title{
  color:$chartTitleTextColor;
  font-family:Arial;
  font-size:18px;
  font-weight:bold;
}

div.main-header{
  width:100%;
  text-align:center;
  font-size:22px;
  font-family:Arial;
  font-weight:bold;
  background-color:rgba(255,255,255,.4);
  color:#000000;
  padding:10px 0;
  margin-bottom:10px;
}
</style>

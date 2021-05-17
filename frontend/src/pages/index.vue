<template>
  <div class="container" v-loading="loading">
    <el-menu default-active="1" class="el-menu-demo" mode="horizontal" @select="handleSelect">
      <el-menu-item index="1">主页</el-menu-item>
      <el-submenu index="2">
        <template slot="title">地区</template>
        <el-submenu index="2-1" :popper-append-to-body="popper">
          <template slot="title">国内</template>
          <div class="sub-menu">
            <div v-for="item in chinaList" :key="item.value" :index="item.value">
              <el-submenu :index="item.value" v-if="item.children">
                <template slot="title">{{item.label}}</template>
                <div class="sub-menu">
                  <el-menu-item
                    v-for="city in item.children"
                    :key="city.value"
                    :index="city.value"
                  >{{city.label}}</el-menu-item>
                </div>
              </el-submenu>
              <el-menu-item :index="item.value" v-else>{{item.label}}</el-menu-item>
            </div>
          </div>
        </el-submenu>
        <el-submenu index="2-2" :popper-append-to-body="popper">
          <template slot="title">国外</template>
          <div class="sub-menu">
            <el-menu-item
              v-for="country in worldList"
              :key="country.value"
              :index="country.value"
            >{{country.label}}</el-menu-item>
          </div>
        </el-submenu>
      </el-submenu>
      <el-menu-item index="3">上传数据</el-menu-item>
      <el-menu-item index="4">下载数据</el-menu-item>
    </el-menu>
    <el-carousel height="550px" v-show="showIndex==1">
      <el-carousel-item>
        <div class="chart" id="chart1"></div>
      </el-carousel-item>
      <el-carousel-item>
        <div class="chart" id="chart2"></div>
      </el-carousel-item>
      <el-carousel-item>
        <div class="chart" id="chart3"></div>
      </el-carousel-item>
      <el-carousel-item>
        <div class="chart" id="chart10"></div>
      </el-carousel-item>
      <el-carousel-item>
        <div class="chart" id="chart6"></div>
      </el-carousel-item>
      <el-carousel-item>
        <div class="chart" id="chart7"></div>
      </el-carousel-item>
      <el-carousel-item>
        <div class="chart" id="chart8"></div>
      </el-carousel-item>
      <el-carousel-item>
        <div class="chart" id="chart9"></div>
      </el-carousel-item>
    </el-carousel>
    <div class="box" v-show="showIndex==2">
      <el-carousel height="550px" v-show="worldChart">
        <el-carousel-item>
          <div class="chart" id="chart4"></div>
        </el-carousel-item>
        <el-carousel-item>
          <div class="chart" id="chart5"></div>
        </el-carousel-item>
      </el-carousel>
      <el-carousel height="550px" v-show="provinceChart">
        <el-carousel-item>
          <div class="chart" id="prochart1"></div>
        </el-carousel-item>
        <el-carousel-item>
          <div class="chart" id="prochart2"></div>
        </el-carousel-item>
        <el-carousel-item>
          <div class="chart" id="prochart3"></div>
        </el-carousel-item>
      </el-carousel>
      <el-carousel height="550px" v-show="cityChart">
        <el-carousel-item>
          <div class="chart" id="citychart1"></div>
        </el-carousel-item>
        <el-carousel-item>
          <div class="chart" id="citychart2"></div>
        </el-carousel-item>
      </el-carousel>
    </div>
    <div class="box" v-show="showIndex == 3">
      <inputBox v-if="showInput"></inputBox>
      <loginBox @updateInput="show" v-else></loginBox>
    </div>
    <div class="box download" v-show="showIndex==4">
      <el-form>
        <el-form-item label="截止时间">
          <el-date-picker
            v-model="downloadData.date"
            align="right"
            type="date"
            placeholder="选择日期"
            :picker-options="pickerOptions"
            value-format="yyyy-MM-dd"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="国外地区">
          <el-cascader
            v-model="downloadData.area"
            :options="worldList"
            :props="{ expandTrigger: 'hover' }"
            @change="handleChange"
          ></el-cascader>
        </el-form-item>
        <el-form-item label="国内地区">
          <el-cascader
            :options="chinaList"
            v-model="downloadData.area"
            :props="{expandTrigger:'hover'}"
            @change="handleChange"
          ></el-cascader>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="downloadData.data_type" multiple placeholder="请选择">
            <el-option
              v-for="item in types"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-select v-model="downloadData.level" placeholder="请选择范围">
            <el-option
              v-for="item in levels"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <el-button @click="download">下载</el-button>
    </div>
  </div>
</template>
<script>
import api from "../api/api";
import axios from "axios";
import inputBox from "../components/inputBox";
import loginBox from "../components/login";
axios.defaults.withCredentials = true;

export default {
  name: "index",
  data() {
    return {
      loading: true,
      showIndex: 1,
      popper: false,
      provinceChart: false,
      cityChart: false,
      worldChart: false,
      dialogVisible: false,
      disabled: false,
      file: null,
      showInput: false,
      chinaList: [],
      worldList: [],
      types: [
        { label: "确诊", value: "confirmed" },
        { label: "治愈", value: "cured" },
        { label: "死亡", value: "death" }
      ],
      levels: [
        {
          label: "全省/市",
          value: true
        },
        {
          label: "各省/市",
          value: false
        }
      ],
      downloadData: {
        area: {}
      },
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() > Date.now();
        },
        shortcuts: [
          {
            text: "今天",
            onClick(picker) {
              picker.$emit("pick", new Date());
            }
          },
          {
            text: "昨天",
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24);
              picker.$emit("pick", date);
            }
          },
          {
            text: "一周前",
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit("pick", date);
            }
          }
        ]
      }
    };
  },
  async mounted() {
    const date = this.getDay(-1, "-");
    let globalData = await api.getdata({ date, type: "accumulated" });
    let chinaData = await api.getdata({
      date,
      type: "accumulated",
      country: "china"
    });
    let golbalSomData = await api.getdata({ date, type: "someday" });
    let chinaSomData = await api.getdata({
      date,
      type: "someday",
      country: "china"
    });
    let chinaLine = await api.getLine({
      date,
      type: "accumulated",
      country: "china"
    });
    let worldLine = await api.getLine({ date, type: "accumulated" });
    let somBar = await api.getBar({ date, type: "someday" });
    let allBar = await api.getBar({ date, type: "accumulated" });
    this.drawWorldLine("chart8", "全球累计", worldLine, [
      "累计确诊",
      "累计治愈",
      "累计死亡"
    ]);
    this.drawWorldLine("chart9", "中国累计", chinaLine, [
      "累计确诊",
      "累计治愈",
      "累计死亡"
    ]);
    this.drawWorldBar("chart6", "世界各国累计", allBar, [
      "累计确诊",
      "累计治愈",
      "累计死亡"
    ]);
    this.drawWorldBar("chart7", "世界各国单日新增", somBar, [
      "单日新增确诊",
      "单日新增治愈",
      "单日新增死亡"
    ]);

    globalData = globalData.detail.map(data => {
      return {
        name: data.name,
        value: [data.confirmed, data.cured, data.death]
      };
    });
    chinaData = chinaData.detail.map(data => {
      return {
        name: data.name,
        value: [data.confirmed, data.cured, data.death]
      };
    });
    golbalSomData = golbalSomData.detail.map(data => {
      return {
        name: data.name,
        value: [data.confirmed, data.cured, data.death]
      };
    });
    chinaSomData = chinaSomData.detail.map(data => {
      return {
        name: data.name,
        value: [data.confirmed, data.cured, data.death]
      };
    });
    const worldData = await axios.get("/world.json");
    this.loading = false;
    console.log({ worldData });
    const namemap = worldData.data.namemap;
    const chinamap = worldData.data.chinamap;
    this.chinaList = worldData.data.chinaList;
    this.worldList = worldData.data.worldList;
    globalData = globalData.map(data => {
      return {
        name: namemap[data.name],
        value: data.value
      };
    });
    chinaData = chinaData.map(data => {
      return {
        name: chinamap[data.name],
        value: data.value
      };
    });
    chinaSomData = chinaSomData.map(data => {
      return {
        name: chinamap[data.name],
        value: data.value
      };
    });
    golbalSomData = golbalSomData.map(data => {
      return {
        name: namemap[data.name],
        value: data.value
      };
    });
    // });

    this.drawChart("chart1", namemap, globalData, "全球累计");
    this.drawChina("chart3", "中国累计", chinamap, chinaData);
    this.drawChina("chart10", "中国单日新增", chinamap, chinaSomData);
    this.drawChart("chart2", namemap, golbalSomData, "全球单日新增");
  },
  methods: {
    handleRemove(file) {
      console.log(file);
    },
    handleDownload(file) {
      console.log(file);
      let res = api.postFile(file.raw);
      this.file = res;
    },
    handleChange(value) {
      console.log({ value });
    },
    show() {
      this.showInput = true;
    },
    async handleSelect(key, keyPath) {
      this.loading = true;
      if (keyPath.length > 1) {
        this.showIndex = keyPath[0];
      } else {
        if (key == 3 || key == 4) {
          this.loading = false;
        }else if(this.chinaList.length > 0){
          this.loading = false;
        }
        this.showIndex = key;
      }
      if (keyPath[1] === "2-2") {
        this.worldChart = true;
        this.provinceChart = false;
        this.cityChart = false;
        let country = this.worldList.filter(item => item.value === keyPath[2]);
        country = country[0].name;
        let somData = await api.getLine({
          date: this.getDay(-1, "-"),
          type: "someday",
          country
        });
        let allData = await api.getLine({
          date: this.getDay(-1, "-"),
          type: "accumulated",
          country
        });
        this.drawWorldLine("chart4", "单日", somData, [
          "单日新增确诊",
          "单日新增治愈",
          "单日新增死亡"
        ]);
        this.drawWorldLine("chart5", "累计", allData, [
          "累计确诊",
          "累计治愈",
          "累计死亡"
        ]);
        this.loading = false;
      }
      if (keyPath[1] === "2-1") {
        this.worldChart = false;
        let pro = this.chinaList.filter(item => item.value === keyPath[2]);
        let city = [];
        if (keyPath.length === 4) {
          city = pro[0]["children"].filter(city => city.value === keyPath[3]);
        }
        let province = pro[0].label;
        if (city.length !== 0) {
          if (city[0].label === "不包括市") {
            this.provinceChart = true;
            this.cityChart = false;
            let somProLin = await api.getLine({
              date: this.getDay(-1, "-"),
              type: "someday",
              country: "china",
              province
            });
            let allProLin = await api.getLine({
              date: this.getDay(-1, "-"),
              type: "accumulated",
              country: "china",
              province
            });
            let provinceBar = await api.getBar({
              date: this.getDay(-1, "-"),
              type: "accumulated",
              country: "china",
              province
            });
            if (provinceBar.varying.length > 0) {
              provinceBar.varying = provinceBar.varying.map(item => {
                let cities = pro[0].children;
                let city = cities.filter(city => {if(city.name === item){
                  return city[0].label
                }});
                // let label = city[0].label;
                return city;
              });
              this.drawWorldBar("prochart3", "省各市", provinceBar, [
                "累计确诊",
                "累计治愈",
                "累计死亡"
              ]);
            }
            this.drawWorldLine("prochart1", "省累计", allProLin, [
              "累计确诊",
              "累计治愈",
              "累计死亡"
            ]);
            this.drawWorldLine("prochart2", "省单日", somProLin, [
              "单日新增确诊",
              "单日新增治愈",
              "单日新增死亡"
            ]);
            this.loading = false;
          } else {
            this.cityChart = true;
            this.provinceChart = false;
            let somCityLin = await api.getLine({
              date: this.getDay(-1, "-"),
              type: "someday",
              country: "china",
              province,
              city: city[0].label.substring(0, city[0].label.length - 1)
            });
            let allCityLin = await api.getLine({
              date: this.getDay(-1, "-"),
              type: "accumulated",
              country: "china",
              province,
              city: city[0].label.substring(0, city[0].label.length - 1)
            });
            this.drawWorldLine("citychart1", "市累计", allCityLin, [
              "累计确诊",
              "累计治愈",
              "累计死亡"
            ]);
            this.drawWorldLine("citychart2", "市单日", somCityLin, [
              "单日新增确诊",
              "单日新增治愈",
              "单日新增死亡"
            ]);
            this.loading = false;
          }
        } else {
          this.provinceChart = true;
          this.cityChart = false;
          let somProLin = await api.getLine({
            date: this.getDay(-1, "-"),
            type: "someday",
            country: "china",
            province
          });
          let allProLin = await api.getLine({
            date: this.getDay(-1, "-"),
            type: "accumulated",
            country: "china",
            province
          });

          this.drawWorldLine("prochart1", "省累计", allProLin, [
            "累计确诊",
            "累计治愈",
            "累计死亡"
          ]);
          this.drawWorldLine("prochart2", "省单日", somProLin, [
            "单日新增确诊",
            "单日新增治愈",
            "单日新增死亡"
          ]);
          this.loading = false;
        }
      }
    },
    async login() {
      await api.login();
    },
    async download() {
      if (JSON.stringify(this.downloadData.area) != "{}") {
        if (this.downloadData.area[0].substring(0, 3) === "2-1") {
          let province = this.chinaList.filter(
            item => item.value === this.downloadData.area[0]
          );
          if (this.downloadData.area.length === 2) {
            if (
              this.downloadData.area[1].substring(
                this.downloadData.area[1].length - 1,
                this.downloadData.area[1].length
              ) != 0
            ) {
              let cities = province[0].children;
              let city = cities.filter(
                city => city.value === this.downloadData.area[1]
              );
              this.downloadData.area = {
                country: "China",
                province: province[0].label,
                city: city[0].label
              };
            } else {
              this.downloadData.area = {
                country: "China",
                province: province[0].label
              };
            }
          } else {
            this.downloadData.area = { province: province[0].label };
          }
        } else {
          let country = this.worldList.filter(
            item => item.value === this.downloadData.area[0]
          );
          this.downloadData.area = { country: country[0].name };
          this.downloadData.level = true;
        }
      }
      if (
        this.downloadData.date &&
        this.downloadData.area &&
        this.downloadData.data_type
      ) {
        await api.download(this.downloadData);
      }
    },
    drawChina(id, seriesName, name, data) {
      let chart = this.$echarts.init(document.getElementById(id));
      chart.setOption({
        title: {
          text: seriesName, // 主标题文本，支持使用 \n 换行
          top: 20, // 定位 值: 'top', 'middle', 'bottom' 也可以是具体的值或者百分比
          left: "center", // 值: 'left', 'center', 'right' 同上
          textStyle: {
            // 文本样式
            fontSize: 25,
            fontWeight: 700,
            color: "#000000"
          }
        },
        visualMap: {
          type: "continuous", // continuous 类型为连续型  piecewise 类型为分段型
          show: true, // 是否显示 visualMap-continuous 组件 如果设置为 false，不会显示，但是数据映射的功能还存在
          min: 0,
          max: 2000,
          // 文本样式
          textStyle: {
            fontSize: 14,
            color: "#000"
          },
          realtime: false, // 拖拽时，是否实时更新
          calculable: true, // 是否显示拖拽用的手柄
          inRange: {
            color: ["#ffffff", "#E80505"] // 图元的颜色
          },
          dimension: 0
        },
        tooltip: {
          backgroundColor: "#ff7f50", //提示标签背景颜色
          textStyle: { color: "#fff" }, //提示标签字体颜色
          formatter: function(val) {
            if (val.data !== undefined) {
              return (
                val.data.name +
                "<br/>确诊人数: " +
                val.data.value[0] +
                "<br/>治愈人数:" +
                val.data.value[1] +
                "<br/>死亡人数:" +
                val.data.value[2]
              );
            } else {
              return val.name + ":no attainable data";
            }
          }
        },
        series: [
          {
            type: "map",
            mapType: "china",
            label: {
              normal: {
                show: true, //显示省份标签
                textStyle: { color: "#c71585" } //省份标签字体颜色
              },
              emphasis: {
                //对应的鼠标悬浮效果
                show: true,
                textStyle: { color: "#800080" }
              }
            },
            itemStyle: {
              normal: {
                borderWidth: 0.5, //区域边框宽度
                borderColor: "#009fe8", //区域边框颜色
                areaColor: "#ffefd5" //区域颜色
              },
              emphasis: {
                borderWidth: 0.5,
                borderColor: "#4b0082",
                areaColor: "#ffdead"
              }
            },
            nameMap: name,
            data: data
          }
        ]
      });
    },
    drawChart(id, name, data, seriesName) {
      let chart = this.$echarts.init(document.getElementById(id));
      window.addEventListener("resize", function() {
        chart.resize();
      });
      chart.setOption({
        title: {
          text: seriesName, // 主标题文本，支持使用 \n 换行
          top: 20, // 定位 值: 'top', 'middle', 'bottom' 也可以是具体的值或者百分比
          left: "center", // 值: 'left', 'center', 'right' 同上
          textStyle: {
            // 文本样式
            fontSize: 25,
            fontWeight: 700,
            color: "#000000"
          }
        },
        tooltip: {
          trigger: "item", // 触发类型, 数据项图形触发，主要在散点图，饼图等无类目轴的图表中使用
          // 提示框浮层内容格式器，支持字符串模板和回调函数两种形式
          // 使用函数模板  传入的数据值 -> value: number | Array
          formatter: function(val) {
            if (val.data !== undefined) {
              return (
                val.data.name +
                "<br/>确诊人数: " +
                val.data.value[0] +
                "<br/>治愈人数:" +
                val.data.value[1] +
                "<br/>死亡人数:" +
                val.data.value[2]
              );
            } else {
              return val.name + ":no attainable data";
            }
          }
        },
        // 视觉映射组件
        visualMap: {
          type: "continuous", // continuous 类型为连续型  piecewise 类型为分段型
          show: true, // 是否显示 visualMap-continuous 组件 如果设置为 false，不会显示，但是数据映射的功能还存在
          min: 0,
          max: 500000,
          // 文本样式
          textStyle: {
            fontSize: 14,
            color: "#000"
          },
          realtime: false, // 拖拽时，是否实时更新
          calculable: true, // 是否显示拖拽用的手柄
          inRange: {
            color: ["#ffffff", "#E80505"] // 图元的颜色
          },
          dimension: 0
        },
        series: [
          {
            type: "map", // 类型
            // 系列名称，用于tooltip的显示，legend 的图例筛选 在 setOption 更新数据和配置项时用于指定对应的系列
            name: seriesName,
            mapType: "world", // 地图类型
            // 是否开启鼠标缩放和平移漫游 默认不开启 如果只想要开启缩放或者平移，可以设置成 'scale' 或者 'move' 设置成 true 为都开启
            roam: true,
            // 图形上的文本标签
            label: {
              show: false // 是否显示对应地名
            },
            // 地图区域的多边形 图形样式
            itemStyle: {
              areaColor: "#7B68EE", // 地图区域的颜色 如果设置了visualMap，areaColor属性将不起作用
              borderWidth: 0.5, // 描边线宽 为 0 时无描边
              borderColor: "#000", // 图形的描边颜色 支持的颜色格式同 color，不支持回调函数
              borderType: "solid" // 描边类型，默认为实线，支持 'solid', 'dashed', 'dotted'
            },
            // 高亮状态下的多边形和标签样式
            emphasis: {
              label: {
                show: true, // 是否显示标签
                color: "auto" // 文字的颜色 如果设置为 'auto'，则为视觉映射得到的颜色，如系列色
              },
              itemStyle: {
                areaColor: "#FF6347" // 地图区域的颜色
              }
            },
            nameMap: name,
            data: data
          }
        ]
      });
    },
    drawWorldLine(id, seriesName, data, legendData) {
      let chart = this.$echarts.init(document.getElementById(id));
      chart.setOption({
        title: {
          text: seriesName
        },
        tooltip: {
          trigger: "axis"
        },
        legend: {
          data: legendData
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        xAxis: {
          type: "category",
          boundaryGap: false,
          data: data.date
        },
        yAxis: {
          type: "value"
        },
        series: [
          {
            name: legendData[0],
            type: "line",
            data: data.detail[0]
          },
          {
            name: legendData[1],
            type: "line",
            data: data.detail[1]
          },
          {
            name: legendData[2],
            type: "line",
            data: data.detail[2]
          }
        ]
      });
    },
    drawWorldBar(id, seriesName, data, legendData) {
      let chart = this.$echarts.init(document.getElementById(id));
      chart.setOption({
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow",
            label: {
              show: true
            }
          }
        },
        toolbox: {
          show: true,
          feature: {
            mark: { show: true },
            dataView: { show: true, readOnly: false },
            magicType: { show: true, type: ["line", "bar"] },
            restore: { show: true },
            saveAsImage: { show: true }
          }
        },
        calculable: true,
        legend: {
          data: legendData,
          itemGap: 5
        },
        grid: {
          top: "12%",
          left: "1%",
          right: "10%",
          containLabel: true
        },
        xAxis: [
          {
            type: "category",
            data: data.varying
          }
        ],
        yAxis: [
          {
            type: "value",
            name: seriesName,
            axisLabel: {
              formatter: a => {
                a = +a;
                return isFinite(a)
                  ? this.$echarts.format.addCommas(+a / 1000)
                  : "";
              }
            }
          }
        ],
        dataZoom: [
          {
            show: true,
            start: 94,
            end: 100
          },
          {
            type: "inside",
            start: 94,
            end: 100
          },
          {
            show: true,
            yAxisIndex: 0,
            filterMode: "empty",
            width: 30,
            height: "80%",
            showDataShadow: false,
            left: "93%"
          }
        ],
        series: [
          {
            name: legendData[0],
            type: "bar",
            data: data.detail[0]
          },
          {
            name: legendData[1],
            type: "bar",
            data: data.detail[1]
          },
          {
            name: legendData[2],
            type: "bar",
            data: data.detail[2]
          }
        ]
      });
    },
    getDay(num, str) {
      let today = new Date();
      let nowTime = today.getTime();
      let ms = 24 * 3600 * 1000 * num;
      today.setTime(parseInt(nowTime + ms));
      let oYear = today.getFullYear();
      let oMoth = (today.getMonth() + 1).toString();
      if (oMoth.length <= 1) oMoth = "0" + oMoth;
      let oDay = today.getDate().toString();
      if (oDay.length <= 1) oDay = "0" + oDay;
      return oYear + str + oMoth + str + oDay;
    },
    draw3d(id, data) {
      let chart = this.$echarts.init(document.getElementById(id));
      chart.setOption({
        backgroundColor: "#cdcfd5",
        geo3D: {
          map: "world",
          shading: "lambert",
          light: {
            main: {
              intensity: 5,
              shadow: true,
              shadowQuality: "high",
              alpha: 30
            },
            ambient: {
              intensity: 0
            },
            ambientCubemap: {
              texture: "data-gl/asset/canyon.hdr",
              exposure: 1,
              diffuseIntensity: 0.5
            }
          },
          viewControl: {
            distance: 50,
            panMouseButton: "left",
            rotateMouseButton: "right"
          },
          groundPlane: {
            show: true,
            color: "#999"
          },
          postEffect: {
            enable: true,
            bloom: {
              enable: false
            },
            SSAO: {
              radius: 1,
              intensity: 1,
              enable: true
            },
            depthOfField: {
              enable: false,
              focalRange: 10,
              blurRadius: 10,
              fstop: 1
            }
          },
          temporalSuperSampling: {
            enable: true
          },
          itemStyle: {},

          regionHeight: 2
        },
        visualMap: {
          max: 40,
          calculable: true,
          realtime: false,
          inRange: {
            color: [
              "#313695",
              "#4575b4",
              "#74add1",
              "#abd9e9",
              "#e0f3f8",
              "#ffffbf",
              "#fee090",
              "#fdae61",
              "#f46d43",
              "#d73027",
              "#a50026"
            ]
          },
          outOfRange: {
            colorAlpha: 0
          }
        },
        series: [
          {
            type: "bar3D",
            coordinateSystem: "geo3D",
            shading: "lambert",
            data: data,
            barSize: 0.1,
            minHeight: 0.2,
            silent: true,
            itemStyle: {
              color: "orange",
              opacity: 0.8
            }
          }
        ]
      });
    }
  },
  components: {
    inputBox,
    loginBox
  }
};
</script>

<style scoped>
.container {
  width: 100%;
  height: 100%;
}
.el-carousel__button {
  background-color: grey !important;
}

.chart {
  width: 100%;
  height: 95%;
  background-size: 100% 100%;
}
.sub-menu {
  height: 500px;
  overflow: scroll;
}
.box {
  width: 100%;
  margin: 0 auto;
}
.download {
  margin: 5% auto;
  width: fit-content;
}
</style>
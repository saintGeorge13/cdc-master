<template>
  <div class="input-box">
    <el-form class="demo-form-inline">
      <el-form-item label="记录日期">
        <el-date-picker
          v-model="date"
          value-format="yyyy-MM-dd"
          align="right"
          type="date"
          placeholder="选择日期"
        ></el-date-picker>
      </el-form-item>
      <el-form-item label="所在地区">
        <el-cascader
          v-model="area"
          :options="chinaList"
          :props="{ expandTrigger: 'hover' }"
          @change="handleChange"
        ></el-cascader>
      </el-form-item>
      <el-form-item label="所在国家">
        <el-cascader
          v-model="area"
          :options="worldList"
          :props="{ expandTrigger: 'hover' }"
          @change="handleChange"
        ></el-cascader>
      </el-form-item>
      <el-form-item>
        <el-input placeholder="请输入确诊人数" type="number" v-model="inputInfo.detail.confirmed"></el-input>
      </el-form-item>
      <el-form-item>
        <el-input placeholder="请输入治愈人数" type="number" v-model="inputInfo.detail.cured"></el-input>
      </el-form-item>
      <el-form-item>
        <el-input placeholder="请输入死亡人数" type="number" v-model="inputInfo.detail.death"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button @click="upload">上传</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import axios from "axios";
axios.defaults.withCredentials = true;
import api from "../api/api";

export default {
  name: "inputBox",
  props: {},
  data() {
    return {
      pickerOptions: {
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
      },
      date:"",
      chinaList: [],
      worldList: [],
      provinces: [],
      area: [],
      inputInfo: {
        detail: {
          confirmed:null,
          cured:null,
          death:null
        }
      }
    };
  },
  async mounted() {
    await this.getProvinces();
  },
  methods: {
    async getProvinces() {
      const worldData = await axios.get("/world.json");
      this.chinaList = worldData.data.chinaList;
      this.worldList = worldData.data.worldList;
      this.provinces = worldData.data.chinamap;
    },
    handleChange(value) {
      let area = value;
      if (area[0].substring(0, 3) === "2-1") {
        let province = this.chinaList.filter(item => item.value === area[0]);
        let pro = null;
        Object.keys(this.provinces).forEach(value => {
          if (this.provinces[value] === province[0].label) {
            pro = value;
          }
        });
        if (this.area.length === 2) {
          if (area[1].substring(area[1].length - 1, area[1].length) != 0) {
            let cities = province[0].children;
            let city = cities.filter(city => city.value === area[1]);
            this.inputInfo.area = {
              country: "china",
              province: pro,
              city: city[0].name
            };
          } else {
            this.inputInfo.area = {
              country: "china",
              province: pro
            };
          }
        } else {
          this.inputInfo.area = { country: "china", province: pro };
        }
      } else {
        let country = this.worldList.filter(item => item.value === area[0]);
        this.inputInfo.area = { country: country[0].name };
      }
    },
    async upload() {
      if (
        this.inputInfo.detail.confirmed &&
        this.inputInfo.detail.cured &&
        this.inputInfo.detail.death
      ) {
        this.inputInfo.date = {
          year:this.date.substring(0,4),
          month:this.date.substring(5,7),
          day:this.date.substring(8,10)
        }
        let res = await api.postData({data:[this.inputInfo]});
        if (res.code === 1) {
          alert(res.message);
        } else {
          alert(res.message);
        }
      }
    }
  }
};
</script>

<style scoped>
.input-box {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 5% auto;
  width: fit-content;
}
</style>
# case-vue

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


### VUE Api
- `v-bind`
- 绑定变量、可算写成 `:` 或者 `.` 

```html
 <div :id="text"></div>
```
```html
<!-- class bind -->
<div :class="{ red: isRead }"></div>
<div :class="[classA,classB]"></div>
<div :class="[classA, {classB:isB,classC:isC}]"></div>

<!-- style bind -->
<div :style="{ fontsize: size + 'px'}"></div>
<div :style="[styleObjA, styleObjB]"></div>
```
- `v-text`
- 绑定标签内显示内容

```html
<div v-text="text">{{text}}</div>
```

- `v-html`
- 以html渲染变量内容

```html
<div v-html="html"></div>
```

- `v-show`
- 隐藏节点显示

```html
<div v-show="flase"></div>
<!-- 代码说明：相当于display：none，虽然不进行节点渲染，但是dom对象一直存在，适用于频繁切换的场景 -->
```
- `v-if`
- 隐藏节点的显示 

```html
<div v-if="true"></div>
<!-- 代码说明：相当于appendChild，removeChild，直接将dom对象添加或者删除，适用于不频繁切换的场景，与v-if配合使用的有，v-else，v-if-else -->
```
  
- `v-for`
- 循环产生同一个组件

```html
<ul>
<li v-for="item in items" :key="item">{{item.name}}</li>
</ul>
<!-- 代码说明：items是一个数组或者对象，将其中每一项都渲染出一个li，值得注意的是每一个li都需要一个独一无二的key，这样才能保证每次重新渲染的时候，只会更改key产生变化的节点，减少了开销，而且不能使用数组的index作为key，因为数组每一项对应的index会产生变化。 -->

```
  
- `v-on`
- 节点绑定事件、可简写 `@`

```html
<div @click="do"></div>
```

### Vue 相应API

- `computed`
- 接受一个 `getter` 函数、 根据其返回值 返回一个不可变的响应式 `ref` 对象

- `watch`
- 组件监听器 `property` 、 监听特定的数据源、并在会点函数中执行作用。 
```html
<div id="app">
 <button @click="num++">{{num}}</button>
</div>
<script>
 Vue.createapp({
  watch:{
  num:function(n1,n2){
   
 }
 },
  data(){
   return {num:0}
  }
 }).mount("#app")
</script>

```
- `directives`
- 注册自定义的指令,对普通 `dom` 元素进行底层操作，就会用到自定义指令.
  
  

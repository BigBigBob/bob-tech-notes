## 一、**JavaScript 的运行时世界**

### 1.1、 JavaScript 的动态类型

JavaScript 的“动态类型”是指：**变量本身不固定类型，类型由运行时变量当前存放的值决定。**

```js
let value = 10;       // 当前是 number
value = "hello";       // 现在是 string
value = true;         // 现在是 boolean
```

同一个变量可以先后保存不同类型的值，不需要提前声明类型。可以用 `typeof` 在运行时查看：

```js
console.log(typeof 10);      // "number"
console.log(typeof "hello");  // "string"
console.log(typeof true);    // "boolean"
```

需要注意，“动态类型”不等于“没有类型”。JavaScript 中的**值仍然有明确类型**，例如 `number`、`string`、`boolean`、`object` 等；只是变量和类型之间没有永久绑定。

这很灵活，但也可能让错误在运行时才暴露：

```js
function add(a, b) {
  return a + b;
}

add(1, 2);     // 3
add("1", 2);   // "12"，因为发生了类型转换
```

因此实际开发中常用 TypeScript，在 JavaScript 之上增加静态类型检查。



### 1.2、JavaScript 的八种值类型

JavaScript 共有七种基本类型和一种对象类型。

* 基本类型：undefined、null、boolean、number、bigint、string、symbol
* 对象类型：object

下面这些对象的类型都属于object：

```js
{}
[]
new Date()

new Map()
new Set()
```

但是函数比较特殊：

```js
typeof function test() {} // "function"
```

从语言模型上说，函数仍然属于对象；但 `typeof` 专门为函数返回 `"function"`。

常见的 `typeof` 结果：

```js
typeof 123          // "number"
typeof "hello"      // "string"
typeof true         // "boolean"
typeof undefined    // "undefined"
typeof 10n          // "bigint"
typeof Symbol()     // "symbol"
typeof {}           // "object"
typeof []           // "object"
typeof function(){} // "function"
```

一个历史遗留陷阱：typeof null 的返回值是 "object"，这不代表 `null` 真的是对象。它是 JavaScript 早期设计遗留下来的行为。

因此，判断 `null` 通常直接写：value === null。

判断数组则使用：Array.isArray(value)，不要使用：typeof value === "array" ，这个判断条件永远不会成立。



（1）、undefined和null的区别

其中，undefined和null 都可以表达“没有值”，但是他们的语义不同。

undefined：通常表示“尚未提供”或“尚未赋值”。具体参考下面的代码示例：

```js
let result;
console.log(result); // undefined

function greet(name) {
  console.log(name);
}

greet(); // undefined
```

null：通常是开发者主动设置的空值：

```js
const selectedUser = null;
```

总结来说，可以理解为：

* undefined：这里暂时没有值，或者值没有被提供。
* null：这里被明确设置为空。



### 1.3、const和let的区别

`const` 和 `let` 都用来声明变量，核心区别是：**变量能否被重新赋值**。

```js
let age = 18;
age = 19; // 可以

const name = "小明";
name = "小红"; // 报错：不能重新赋值
```

但 `const` 声明的对象或数组，其**内容仍然可以修改**：

```js
const user = { name: "小明" };
user.name = "小红"; // 可以

const numbers = [1, 2];
numbers.push(3); // 可以
```

不能把整个变量换成另一个对象或数组：

```js
user = { name: "小刚" }; // 报错
numbers = [4, 5];        // 报错
```

简单理解：

* `let`：变量之后需要重新赋值时使用。
* `const`：变量不会重新赋值时使用。

通常优先使用 `const`，确定需要重新赋值时再使用 `let`。

两者还有一些共同点：

* 都是块级作用域。
* 都不能在同一作用域内重复声明。
* 声明前访问都会报错。
* `const` 声明时必须立即赋值：

```js
let value;    // 可以
const value;  // 报错
```



### 1.4、===和==的区别

核心区别：

* `==`：宽松相等，比较前可能自动转换类型。
* `===`：严格相等，不转换类型，同时比较类型和值。

```js
5 == "5"   // true，字符串 "5" 被转换成数字
5 === "5"  // false，类型不同
```

更多例子：

```js
0 == false        // true
0 === false       // false

"" == false       // true
"" === false      // false

null == undefined   // true
null === undefined  // false
```

对象和数组比较的是“引用是否为同一个”：

```js
[1, 2] === [1, 2] // false，两个不同的数组对象

const a = [1, 2];
const b = a;

a === b // true，指向同一个数组
```

实际开发中，建议默认使用 `===` 和 `!==`，结果更明确，也能避免隐式类型转换带来的意外。

```js
if (age === 18) {
  // ...
}
```

只有确实需要宽松比较规则，并且清楚类型转换结果时，才考虑使用 `==`。



## 二、作用域与闭包

### 2.1、作用域是什么

作用域决定了一个变量可以在哪些位置被访问。

```js
const appName = "Demo";

function start() {
  const version = "1.0";

  console.log(appName);
  console.log(version);
}

start();

console.log(appName);
// console.log(version); // ReferenceError
```

这里：

* `appName` 位于外层作用域，内部函数可以访问它。
* `version` 位于 `start` 的函数作用域，函数外部不能访问它。

可以画成：

```text
全局作用域
├── appName
└── start
    └── 函数作用域
        └── version
```

当 JavaScript 查找一个变量时，会从当前位置开始逐层向外查找：

```text
当前作用域 → 外层作用域 → 更外层作用域 → 全局作用域
```

这个查找关系称为**作用域链**。



（1）、JavaScript 中常见的作用域

* 全局作用域，在普通脚本的最外层声明：

```js
const appName = "My App";
```

真实项目通常会使用模块，因此每个模块拥有自己的顶层作用域，而不是让所有变量真正进入全局环境。

* 函数作用域，函数参数和函数内部声明的变量属于函数：

```js
function calculate(price, count) {
  const total = price * count;
  return total;
}
```

这里的 `price`、`count` 和 `total` 都只能在 `calculate` 内部访问。

* 块级作用域，由一对花括号形成，例如：

```js
if (true) {
  const message = "hello";
  let count = 1;
}

// message 和 count 在这里不可访问
```



（2）、变量遮蔽

内层作用域可以声明与外层同名的变量：

```js
const config = "global config";

function initialize() {
  const config = "local config";
  console.log(config);
}

initialize();
console.log(config);
```

输出：

```text
local config
global config
```

函数内部的 `config` 遮蔽了外层的 `config`。这叫作变量遮蔽，也称 shadowing。



（3）、`var`、`let` 和 `const` 的作用域差异

现代项目主要使用 `const` 和 `let`，但旧项目、编译输出以及依赖代码中仍可能出现 `var`。

`let` 和 `const` 是块级作用域

```js
if (true) {
  let count = 1;
  const name = "Alice";
}

// 这里不能访问 count 和 name
```

`var` 是函数作用域

```js
function test() {
  if (true) {
    var count = 1;
  }

  console.log(count);
}

test();
```

输出结果：1

`if` 的花括号没有限制 `var`。在这个例子中，`count` 属于整个 `test` 函数。

如果没有函数包围它：

```js
if (true) {
  var value = 10;
}

console.log(value); // 10
```

这也是为什么现代代码通常避免使用 `var`：它的作用域边界不够直观。



### 2.2、变量提升

JavaScript 在执行一个作用域之前，会先处理该作用域中的声明。

因此某些声明看起来可以在代码出现之前使用。这种现象通常称为**提升**，即 hoisting。

不过，不同声明的提升行为不一样。

（1）、函数声明的提升

使用函数声明时，可以在声明之前调用：

```js
greet();

function greet() {
  console.log("hello");
}
```

可以将其粗略理解成：进入作用域时，JavaScript 已经创建好了 `greet` 函数。

这种行为经常被用于把主要逻辑放在文件上方，把辅助函数放在文件下方：

```js
export function processData(data) {
  const normalized = normalize(data);
  return validate(normalized);
}

function normalize(data) {
  return data.trim();
}

function validate(data) {
  return data.length > 0;
}
```

即使辅助函数写在后面，前面的 `processData` 仍然可以调用它们。

（2）、函数表达式不会像函数声明一样工作

下面的代码会报错：

```js
greet();

const greet = function () {
  console.log("hello");
};
```

箭头函数也是如此：

```js
greet();

const greet = () => {
  console.log("hello");
};
```

因为这里提升的是变量声明，而不是把函数值提前赋给变量。

这两个写法的本质都是：

```js
const greet = 某个函数值;
```

只有执行到赋值语句之后，`greet` 才真正保存了函数。

所以需要写成：

```js
const greet = () => {
  console.log("hello");
};

greet();
```



### 2.3、闭包是什么

先看一个函数返回函数的例子：

```js
function createCounter() {
  let count = 0;

  return function increment() {
    count += 1;
    return count;
  };
}

const counter = createCounter();

console.log(counter()); // 1
console.log(counter()); // 2
console.log(counter()); // 3
```

按照普通直觉，`createCounter()` 已经执行完了，它的局部变量 `count` 似乎也应该消失。

但是返回的 `increment` 函数仍然引用了 `count`，因此 `count` 会继续存在。

这就是闭包：函数 + 函数定义时能够访问的外层词法环境。

可以想象为：

```text
counter
  │
  ▼
increment 函数
  │
  └── 引用 createCounter 作用域中的 count
```

只要 `counter` 还可以被访问，这个闭包及其需要的外层变量就仍然可以被访问。

（1）、每次函数调用都会产生新的词法环境

```js
function createCounter() {
  let count = 0;

  return function () {
    count += 1;
    return count;
  };
}

const first = createCounter();
const second = createCounter();

console.log(first());  // 1
console.log(first());  // 2
console.log(second()); // 1
```

`first` 和 `second` 并不共享 `count`。

因为 `createCounter()` 被调用了两次，每次都会产生一个新的局部环境：

```text
first  → count: 2
second → count: 1
```

也就是说，每次调用都产生独立状态。

（2）、`var` 在循环中的经典闭包问题

```js
const functions = [];

for (var i = 0; i < 3; i++) {
  functions.push(function () {
    console.log(i);
  });
}

functions[0]();
functions[1]();
functions[2]();
```

输出的结果是3，3，3

原因是：

* `var` 是函数作用域，不是块级作用域。
* 三个函数闭包引用的是同一个 `i`。
* 循环结束后，这个 `i` 已经变成 `3`。
* 调用函数时，它们读取到的都是当前的 `i`，不是创建函数时的快照。

使用 `let`：

```js
const functions = [];

for (let i = 0; i < 3; i++) {
  functions.push(function () {
    console.log(i);
  });
}
```

输出的结果是：0，1，2

在 `for` 循环中使用 `let` 时，JavaScript 会为每次迭代创建对应的循环变量绑定。



## 三、函数

### 3.1、创建函数的方式

（1）、函数声明

```js
function add(a, b) {
  return a + b;
}
```

（2）、函数表达式

```js
const add = function (a, b) {
  return a + b;
};
```

这里先创建了一个函数值，再把它赋给变量 `add`。

因为 `add` 是 `const` 变量，所以不能在赋值前调用：

```js
add(2, 3); // ReferenceError

const add = function (a, b) {
  return a + b;
};
```

（3）、箭头函数

```js
const add = (a, b) => {
  return a + b;
};
```

如果函数体只有一个表达式，可以省略花括号和 `return`：

```js
const add = (a, b) => a + b;
```

当只有一个参数时，可以省略参数括号：

```js
const double = value => value * 2;
```

没有参数或有多个参数时，必须保留括号：

```js
const getTime = () => Date.now();

const add = (a, b) => a + b;
```



### 3.2、剩余参数 `...args`

剩余参数可以把多余的实参收集到一个数组中：

```js
function sum(...numbers) {
  let total = 0;

  for (const number of numbers) {
    total += number;
  }

  return total;
}

sum(1, 2, 3);       // 6
sum(1, 2, 3, 4, 5); // 15
```

`numbers` 是一个真正的数组：

```js
Array.isArray(numbers) // true
```

剩余参数也可以和普通参数一起使用：

```js
function log(level, ...messages) {
  console.log(level, messages);
}

log("info", "Server started", "Port:", 3000);
```

level和messages接收到的参数，分别如下：

```text
level    → "info"
messages → ["Server started", "Port:", 3000]
```

剩余参数必须是最后一个参数。



### 3.3、函数没有显式返回值时返回 `undefined`

```js
function greet() {
  console.log("Hello");
}

const result = greet();

console.log(result); // undefined
```



### 3.4、回调函数

作为参数传给另一个函数的函数，通常称为回调函数。

```js
function execute(callback) {
  callback();
}

execute(() => {
  console.log("Executed");
});
```

`execute` 是接收函数，箭头函数是回调函数。



## 四、this的指向

`this` 是 JavaScript 中最容易被误解的机制之一。

先记住重要的一句话：普通函数的 this 通常由调用方式决定，箭头函数的this是由定义位置决定。

### 4.1、普通函数的this

考虑一个对象：

```js
const user = {
  name: "Alice",

  introduce() {
    console.log(this.name);
  }
};

user.introduce(); // "Alice"
```

调用点左侧是 `user`，因此这次调用中的：

```js
this === user
```

可以近似理解成：

```js
introduce.call(user);
```

但 `introduce` 函数并不永久属于 `user`。

```js
const anotherUser = {
  name: "Bob",
  introduce: user.introduce
};

anotherUser.introduce(); // "Bob"
```

同一个函数被不同对象调用时，this的指向也是不一样的：

```text
user.introduce()        → this 是 user
anotherUser.introduce() → this 是 anotherUser
```

### 4.2、箭头函数的this

箭头函数里最关键的一句话是：

> 箭头函数没有自己的 `this`，它使用定义时所在外层作用域的 `this`。

```js
function createArrow() {
  return () => {
    console.log(this.name);
  };
}

const user = {
  name: "小明",
  createArrow
};

const fn = user.createArrow();

fn(); // 小明
```

执行过程是：

1. 调用 `user.createArrow()`
2. `createArrow` 是普通函数，因此它的 `this` 是 `user`
3. 箭头函数创建时，捕获了 `createArrow` 中的 `this`
4. 即使后来单独执行 `fn()`，它仍然使用之前捕获的 `user`



（1）、对象方法中使用箭头函数的坑

```js
const user = {
  name: "小明",

  sayName: () => {
    console.log(this.name);
  }
};

user.sayName();
```

对象字面量 `{}` 不会创建一个新的 `this` 作用域。这个箭头函数会捕获对象外层的 `this`，而不是捕获 `user`。

可以近似理解为：

```js
const outerThis = this;

const user = {
  name: "小明",

  sayName: () => {
    console.log(outerThis.name);
  }
};
```

正确写法应该使用普通方法：

```js
const user = {
  name: "小明",

  sayName() {
    console.log(this.name);
  }
};

user.sayName(); // 小明
```

或者：

```js
const user = {
  name: "小明",

  sayName: function () {
    console.log(this.name);
  }
};
```



（2）、箭头函数适合嵌套回调

箭头函数最初解决的一个重要问题，就是回调函数会丢失外层 `this`。

普通函数回调的问题，参见如下的代码：

```js
const user = {
  name: "小明",

  introduce() {
    setTimeout(function () {
      console.log(this.name);
    }, 1000);
  }
};

user.introduce();
```

调用 `user.introduce()` 时，`introduce` 里的 `this` 是 `user`。

但传给 `setTimeout` 的函数是另外一个普通函数。它被定时器调用时，并不是通过：

```js
user.someFunction();
```

调用，所以其 `this` 不再是 `user`。

但是使用箭头函数就可以解决这个问题：

```js
const user = {
  name: "小明",

  introduce() {
    setTimeout(() => {
      console.log(this.name);
    }, 1000);
  }
};

user.introduce(); // 1 秒后输出“小明”
```

这里：

1. `introduce` 是普通方法
2. `user.introduce()` 使 `introduce` 中的 `this` 成为 `user`
3. 定时器箭头函数捕获 `introduce` 的 `this`
4. 因此回调中仍然可以访问 `user`

在没有箭头函数的时候，过去经常这样写：

```js
const user = {
  name: "小明",

  introduce() {
    const self = this;

    setTimeout(function () {
      console.log(self.name);
    }, 1000);
  }
};
```



## 五、原型、原型链和class

JavaScript 是一门“基于原型”的语言。即使使用 `class`，底层依然主要依靠原型和原型链完成属性共享、方法复用与继承。

先用一句话概括：

> 每个普通对象都可以关联另一个对象作为自己的原型；访问对象属性时，如果对象本身没有，JavaScript 就沿着原型继续查找，直到找到属性或走到 `null`。这条查找路径就是原型链。

### 5.1、原型是什么？

每个普通对象通常都有一个内部原型链接。

```js
const user = {
  name: "Alice"
};
```

可以近似画成：

```text
user
├── 自身属性：name
└── [[Prototype]] ──→ Object.prototype
                         ├── toString
                         ├── valueOf
                         ├── hasOwnProperty
                         └── ...
```

`[[Prototype]]` 是规范中使用的内部概念，不是普通代码直接使用的属性名。

可以通过：

```js
Object.getPrototypeOf(user)
```

读取对象的原型：

```js
Object.getPrototypeOf(user) === Object.prototype
// true
```

#### (1)、属性的查找过程

当执行：

```js
user.name
```

JavaScript 会：

1. 检查 `user` 自己是否有 `name`
2. 找到后直接返回 `"Alice"`

当执行：

```js
user.toString
```

JavaScript 会：

1. 检查 `user` 自己是否有 `toString`
2. 没找到
3. 前往 `user` 的原型
4. 在 `Object.prototype` 上找到 `toString`
5. 返回这个函数

这就是原型链属性查找。

如果当前原型也没有，则继续向上查找，直到遇到：

```js
null
```

完整路径大致是：

```text
当前对象
   ↓
当前对象的原型
   ↓
原型的原型
   ↓
...
   ↓
null
```

到达 `null` 后仍然没找到，就返回：

```js
undefined
```



#### (2)、`in` 和 `Object.hasOwn()` 的区别

请先看下面的这段示例代码：

```js
const parent = {
  type: "父对象"
};

const child = Object.create(parent);
child.name = "子对象";

console.log("name" in child); // true
console.log("type" in child); // true
console.log("toString" in child); // true

console.log(Object.hasOwn(child, "name")); // true
console.log(Object.hasOwn(child, "type")); // false
console.log(Object.hasOwn(child, "toString")); // false
```

* 使用 `in` 会检查：对象自身、整条原型链。
* 使用 `Object.hasOwn()`只检查对象自身。

#### (3)、属性遮蔽

对象可以定义一个与原型属性同名的自身属性：

```js
const user = {
  name: "Alice",

  toString() {
    return this.name;
  }
};

user.toString(); // "Alice"
```

查找 `toString` 时：

1. 先在 `user` 自身找到
2. 不再继续查找 `Object.prototype.toString`

这叫作属性遮蔽。

如果删除自身属性：

```js
delete user.toString;
```

再次访问：

```js
user.toString
```

就会找到原型上的版本。

#### (4)、如何获取对象的原型？

推荐使用：

```js
Object.getPrototypeOf(user);
```

例如：

```js
const user = {};

console.log(
  Object.getPrototypeOf(user) === Object.prototype
); // true
```

也能通过：

```js
user.__proto__
```

读取，但 `__proto__` 是历史遗留访问方式，不推荐在正式代码中依赖它。

推荐写法：

```js
Object.getPrototypeOf(obj);
Object.setPrototypeOf(obj, prototype);
```

不过频繁使用 `Object.setPrototypeOf()` 修改现有对象的原型，可能影响 JavaScript 引擎优化。设计对象结构时，通常应当在创建阶段确定原型。



### 5.2、手动创建原型关系

#### (1)、`Object.create`

**`Object.create()`** 的作用是：**创建一个新对象，并将新对象的 `__proto__`（内部原型指针）指向传入的参数对象**。

参见下面的在这段代码：

```js
const animal = {
  breathe() {
    console.log("Breathing");
  }
};

const dog = Object.create(animal);

dog.name = "Lucky";
dog.bark = function () {
  console.log("Woof");
};
```

原型关系：

```text
dog
├── name
├── bark
└── [[Prototype]] ──→ animal
                       └── breathe
```



### 5.3、原型链

#### (1)、多层原型链

详细参见下面这段代码：

```js
function User(name) {
  this.name = name;
}

User.prototype.introduce = function () {
  console.log(this.name);
};

const alice = new User("Alice");
```

原型链大致是：

```text
alice
  ↓ [[Prototype]]
User.prototype
  ↓ [[Prototype]]
Object.prototype
  ↓ [[Prototype]]
null
```

读取：alice.name ，在 `alice` 自身找到。

读取：alice.introduce，在 `User.prototype` 找到。

读取：alice.toString，在：

```text
alice             没找到
User.prototype    没找到
Object.prototype  找到
```

#### (2)、数组的原型链

```js
const items = [1, 2, 3];
```

`items` 自己并没有保存一份 `map`：

```js
Object.hasOwn(items, "map"); // false
```

但可以调用：

```js
items.map(item => item * 2);
```

因为原型链大致是：

```text
items
  ↓
Array.prototype
  ├── map
  ├── filter
  ├── reduce
  ├── push
  └── ...
  ↓
Object.prototype
  ├── toString
  └── ...
  ↓
null
```

验证：

```js
Object.getPrototypeOf(items) === Array.prototype
  // true
```

这解释了为什么所有数组都能共享数组方法，而不需要每个数组单独保存一份 `map`。

#### (3)、函数的原型链

```js
function greet() {
}
```

`greet` 本身是一个函数对象，因此：

```js
Object.getPrototypeOf(greet) === Function.prototype
   // true
```

这就是它为什么能调用：

```js
greet.call(...)
greet.apply(...)
greet.bind(...)
```

因为这些方法通常来自：

```js
Function.prototype
```

关系大致是：

```text
greet 函数对象
  ↓
Function.prototype
  ↓
Object.prototype
  ↓
null
```

#### (4)、instanceof检查原型链

```js
class Animal {
}

class Dog extends Animal {
}

const dog = new Dog();
```

结果：

```js
dog instanceof Dog;    // true
dog instanceof Animal; // true
dog instanceof Object; // true
```

`instanceof` 的核心问题是：构造函数的 prototype 是否出现在对象的原型链上？

例如：dog instanceof Animal

近似检查：Animal.prototype 是否存在于 dog 的原型链？

因为：

```text
dog
↓
Dog.prototype
↓
Animal.prototype
```

所以结果为 `true`。



### 5.4、class

#### (1)、基本类定义

参见如下的示例代码：

```js
class User {
  //
负责初始化实例自身属性
  constructor(name) {
    this.name = name;
  }
  
  //introduce函数会被定义在：User.prototype
  introduce() {
    console.log(`I am ${this.name}`);
  }
}

const alice = new User("Alice");

alice.introduce();
```

可以验证：

```js
Object.hasOwn(alice, "name"); // true

Object.hasOwn(alice, "introduce"); // false

Object.hasOwn(User.prototype, "introduce"); // true
```

所以：

```js
alice.introduce === User.prototype.introduce
  // true
```

`​`

#### (2)、extends

详细参见如下的代码：

```js
class Animal {
  constructor(name) {
    this.name = name;
  }

  introduce() {
    console.log(`I am ${this.name}`);
  }

  move() {
    console.log(`${this.name} is moving`);
  }
}

class Dog extends Animal {
  bark() {
    console.log(`${this.name}: Woof`);
  }
}

const dog = new Dog("Lucky");

dog.introduce();
dog.move();
dog.bark();
```

`Dog` 没有定义 `introduce` 和 `move`，但实例可以通过原型链找到它们。

原型关系大致是：

```text
dog
  ↓
Dog.prototype
  ├── bark
  ↓
Animal.prototype
  ├── introduce
  ├── move
  ↓
Object.prototype
  ↓
null
```

#### (3)、子类构造函数与super()

```js
class Dog extends Animal {
  constructor(name, breed) {
    super(name);
    this.breed = breed;
  }
}
```

子类构造函数必须在使用 `this` 前调用：

```js
super(...)
```

`super(name)` 调用父类构造函数，并让父类初始化当前这个实例。

注意，它不是创建一个单独的 `Animal` 实例再塞进 `Dog`。

`Dog` 实例仍然只有一个：

```text
同一个 dog 实例
├── name 由 Animal 构造函数初始化
└── breed 由 Dog 构造函数初始化
```

#### (4)、Getter和Setter

Getter函数的示例代码如下：

```js
class Rectangle {
  constructor(width, height) {
    this.width = width;
    this.height = height;
  }

  get area() {
    return this.width * this.height;
  }
}

const rectangle = new Rectangle(4, 5);

console.log(rectangle.area); // 20
```

访问形式看起来是属性：rectangle.area，但背后会执行 getter 函数。

不要写成：rectangle.area()，Getter 适合计算派生属性。



Setter函数的示例代码如下：

```js
class User {
  constructor(name) {
    this._name = name;
  }

  get name() {
    return this._name;
  }

  set name(value) {
    this._name = value.trim();
  }
}

const user = new User("Alice");

user.name = "  Bob  ";

console.log(user.name); // "Bob"
```

赋值：user.name = "Bob";   会调用 setter。

读取：user.name，会调用 getter。

`_name` 只是命名约定，并不是真正私有。



## 六、数组、集合、迭代器

### 6.1、数组的基本类型

```js
const users = ["Alice", "Bob", "Charlie"];

// 数组通过数字索引访问元素：
users[0]; // "Alice"
users[1]; // "Bob"
users[2]; // "Charlie"

// 数组也是对象：
typeof users // "object"

// 判断一个值是否是数组，应使用 Array.isArray
Array.isArray(users) // true
```

### 6.2、会修改原数组的方法

#### (1)、 `push` 和 `pop`

push：在数组尾部添加元素，并返回新长度：

```js
const items = ["a", "b"];
// 注意 push 返回的是长度，不是数组
const length = items.push("c");

console.log(items);  // ["a", "b", "c"]
console.log(length); // 3
```

pop：删除并返回最后一个元素：

```js
const items = ["a", "b", "c"];

const last = items.pop();

console.log(last);  // "c"
console.log(items); // ["a", "b"]
```

#### (2)、`unshift` 和 `shift`

unshift：向数组开头添加元素：

```js
const items = ["b", "c"];

items.unshift("a");

console.log(items); // ["a", "b", "c"]
```

shift：删除并返回第一个元素：

```js
const items = ["a", "b", "c"];

const first = items.shift();

console.log(first); // "a"
console.log(items); // ["b", "c"]
```

因为开头的其他元素通常需要重新调整索引，频繁使用 `shift` 和 `unshift` 处理大数组可能比尾部操作成本更高

#### (3)、`splice`

`splice` 可以删除、插入或替换元素，并且会修改原数组。

```js
array.splice(startIndex, deleteCount, ...newItems)
```

删除：

```js
const items = ["a", "b", "c", "d"];

const removed = items.splice(1, 2);

console.log(removed); // ["b", "c"]
console.log(items);   // ["a", "d"]
```

插入：

```js
const items = ["a", "d"];

items.splice(1, 0, "b", "c");

console.log(items); // ["a", "b", "c", "d"]
```

替换：

```js
const items = ["a", "b", "c"];

items.splice(1, 1, "B");

console.log(items); // ["a", "B", "c"]
```

#### (4)、 `sort`

`sort` 会修改原数组：

```js
const numbers = [3, 1, 2];

const result = numbers.sort();

console.log(numbers); // [1, 2, 3]
console.log(result === numbers); // true
```

数字排序应提供比较函数：

```js
numbers.sort((a, b) => a - b);
```

升序：

```js
(a, b) => a - b
```

降序：

```js
(a, b) => b - a
```

### 6.3、返回新数组的方法

#### (1)、 `slice`

`slice` 截取一部分元素，返回新数组，不修改原数组。

```js
const items = ["a", "b", "c", "d"];

const selected = items.slice(1, 3);

console.log(selected); // ["b", "c"]
console.log(items);    // ["a", "b", "c", "d"]
```

范围是：包含开始索引，不包含结束索引。

#### (2)、 `concat`

```js
const first = [1, 2];
const second = [3, 4];

const combined = first.concat(second);

console.log(combined); // [1, 2, 3, 4]
```

也可以使用展开语法：

```js
const combined = [
  ...first,
  ...second
];
```

两种方式都不会修改原数组。



### 6.4、转换数组

#### (1)、 `map`

`map` 把每个元素转换成一个新值，并返回新数组。

```js
const numbers = [1, 2, 3];

const doubled = numbers.map(number => number * 2);

console.log(doubled); // [2, 4, 6]
```

转换对象：

```js
const names = users.map(user => user.name);
```

转换结构：

```js
const options = users.map(user => ({
  label: user.name,
  value: user.id
}));
```

`map` 回调的返回值非常重要。

```js
// 错误示例
const names = users.map(user => {
  user.name;
});

// 因为没有 return，结果是：
[undefined, undefined, ...]

// 正确示例
const names = users.map(user => {
  return user.name;
});
// 或者：
const names = users.map(user => user.name);
```

#### (2)、 `filter`

`filter` 保留回调返回真值的元素：

```js
const activeUsers = users.filter(user => user.active);
```

原数组不变，返回新数组。

过滤空值的常见写法：

```js
const values = [0, 1, null, 2, undefined, 3];

const result = values.filter(Boolean);
// 结果
[1, 2, 3]
```

#### (3)、 `flat`

```js
const nested = [
  [1, 2],
  [3, 4]
];

nested.flat(); // [1, 2, 3, 4]
```

默认只展开一层：

```js
[1, [2, [3]]].flat();
// [1, 2, [3]]
```

指定深度：

```js
[1, [2, [3]]].flat(2);
// [1, 2, 3]
```

完全展开常见写法：

```js
nested.flat(Infinity);
```

但非常深或循环引用的结构需要谨慎。

#### (4)、 `flatMap`

`flatMap` 近似相当于先 `map`，再展开一层：

```js
const sentences = [
  "hello world",
  "javascript language"
];

const words = sentences.flatMap(
  sentence => sentence.split(" ")
);
```

结果：

```js
[
  "hello",
  "world",
  "javascript",
  "language"
]
```

近似等价：

```js
sentences
  .map(sentence => sentence.split(" "))
  .flat();
```

### 6.5、Map

#### (1)、`Map` 的基本方法

```js
const map = new Map();
```

添加或更新：

```js
map.set("name", "Alice");
map.set("age", 20);
```

读取：

```js
map.get("name"); // "Alice"
```

判断键是否存在：

```js
map.has("name"); // true
```

删除：

```js
map.delete("name");
```

清空：

```js
map.clear();
```

数量：

```js
map.size
```

### 6.6、迭代器

#### (1)、迭代器的 `next()`

迭代器是一个拥有 `next()` 方法的对象。

每次调用返回：

```js
{
  value: 某个值,
  done: 是否结束
}
```

例如：

```js
const iterator = ["a", "b"][Symbol.iterator]();

iterator.next();
// { value: "a", done: false }

iterator.next();
// { value: "b", done: false }

iterator.next();
// { value: undefined, done: true }
```

`for...of` 内部会不断调用 `next()`，直到：

```js
done === true
```

#### (2)、`Symbol.iterator`

一个对象如果拥有：

```js
object[Symbol.iterator]()
```

并且该方法返回迭代器，那么它就是可迭代对象。

手动实现：

```js
const range = {
  start: 1,
  end: 3,

  [Symbol.iterator]() {
    let current = this.start;
    const end = this.end;

    return {
      next() {
        if (current <= end) {
          const value = current;
          current += 1;

          return {
            value,
            done: false
          };
        }

        return {
          value: undefined,
          done: true
        };
      }
    };
  }
};
```

现在可以：

```js
for (const number of range) {
  console.log(number);
}
```

#### (3)、可迭代对象和迭代器不是完全相同的概念

* 可迭代对象：能够创建迭代器；
* 迭代器：通过 next() 逐个产生结果；

数组是可迭代对象：

```js
const array = [1, 2, 3];
```

调用：

```js
array[Symbol.iterator]()
```

得到一个迭代器。

一个可迭代对象通常可以被多次遍历，因为每次都会创建新迭代器：

```js
for (const value of array) {
}

for (const value of array) {
}
```

而某个具体迭代器通常是有状态、一次性向前移动的：

```js
const iterator = array[Symbol.iterator]();

iterator.next();
iterator.next();
```

它记住了当前遍历位置。



## 七、模块与项目组织方式

### 7.1、为什么需要模块

如果所有代码都写在一个文件里：

```js
const users = [];
const config = {};
const cache = new Map();

function createUser() {
}

function deleteUser() {
}

function startServer() {
}
```

随着项目增大，会出现：

* 变量名冲突
* 内部实现暴露
* 文件职责混乱
* 依赖关系难以理解
* 测试困难
* 修改影响范围不清楚

模块把程序拆成若干文件，并显式定义：

```text
这个文件向外提供什么
这个文件依赖什么
```

例如：

```text
src/
├── config.js
├── user-service.js
├── user-repository.js
└── index.js
```

每个文件拥有独立的模块作用域。

```js
// config.js
const secret = "internal";

export const config = {
  port: 3000
};
```

其他模块只能访问导出的 `config`，不能直接访问内部的 `secret`。

### 7.2、ES Modules

ES Modules，简称 ESM，是 JavaScript 标准模块系统，使用：import、export

Node.js 目前稳定支持 ESM，并同时保留 CommonJS 模块系统。[Node.js ESM 官方文档](https://nodejs.org/api/esm.html)​

### 7.3、命名导出

```js
// math.js
export function add(a, b) {
  return a + b;
}

export function subtract(a, b) {
  return a - b;
}

export const PI = 3.14159;
```

导入：

```js
// app.js
import {
  add,
  subtract,
  PI
} from "./math.js";

console.log(add(2, 3));
```

花括号中的名称必须与导出名称对应：

```js
import {
  add
} from "./math.js";
```

以下名称不存在时，模块加载通常会失败：

```js
import {
  multiply
} from "./math.js";
```

#### (1)、先声明，再统一导出

下面两种写法作用相同。

直接导出：

```js
export function add(a, b) {
  return a + b;
}

export const PI = 3.14159;
```

统一导出：

```js
function add(a, b) {
  return a + b;
}

const PI = 3.14159;

export {
  add,
  PI
};
```

真实项目经常先定义实现，再在文件底部集中导出。

#### (2)、导入时重命名

```js
import {
  add as addNumbers
} from "./math.js";
```

这里：

```text
原导出名：add
当前文件变量名：addNumbers
```

使用：

```js
addNumbers(2, 3);
```

常用于解决命名冲突：

```js
import {
  create as createUser
} from "./user.js";

import {
  create as createOrder
} from "./order.js";
```

#### (3)、导出时重命名

```js
function internalAdd(a, b) {
  return a + b;
}

export {
  internalAdd as add
};
```

其他文件看到的是：

```js
import {
  add
} from "./math.js";
```

不会看到 `internalAdd` 这个名称。

### 7.4、默认导出

#### (1)、`export default`

一个模块最多有一个默认导出：

```js
// logger.js
export default function createLogger() {
  return {
    log(message) {
      console.log(message);
    }
  };
}
```

导入默认导出时不使用花括号：

```js
import createLogger from "./logger.js";
```

默认导入名称由导入方决定：

```js
import makeLogger from "./logger.js";
```

`makeLogger` 和 `createLogger` 都可以，因为默认导出并不要求导入方使用固定本地名称。

#### (2)、默认导出与命名导出可以同时存在

```js
// logger.js
export const LOG_LEVEL = "info";

export function formatMessage(message) {
  return `[LOG] ${message}`;
}

export default function createLogger() {
}
```

导入：

```js
import createLogger, {
  LOG_LEVEL,
  formatMessage
} from "./logger.js";
```

其中：

```text
createLogger               → 默认导入
LOG_LEVEL、formatMessage   → 命名导入
```

#### (3)、花括号的意义

```js
// 表示导入默认导出
import logger from "./logger.js";

// 表示导入一个名字必须叫 logger 的命名导出
import {
  logger
} from "./logger.js";
```

两者完全不同。

假设：

```js
export default function logger() {
}
```

只能这样导入：

```js
import logger from "./logger.js";
```

### 7.5、命名空间导入

`import * as`

```js
import * as math from "./math.js";
```

假设 `math.js` 导出：

```js
export function add() {
}

export function subtract() {
}

export const PI = 3.14159;
```

那么可以：

```js
math.add(2, 3);
math.subtract(5, 2);
console.log(math.PI);
```

`math` 是模块命名空间对象，包含该模块的导出。

这种写法在工具模块中很常见：

```js
import * as path from "node:path";
```

不过命名空间对象不是普通的、任意可修改配置对象。导入方不能把模块导出重新赋值。

### 7.6、重新导出

#### (1)、从另一个模块直接导出

```js
// index.js
export {
  createUser,
  deleteUser
} from "./user-service.js";
```

这同时完成了：从 user-service.js 获取导出，再从 index.js 对外导出。

如果当前模块自己不需要使用 `createUser`，就不必先导入再导出。

#### (2)、`export *`

```js
export * from "./user-service.js";
export * from "./order-service.js";
```

它会重新导出目标模块的命名导出。但是默认导出通常不会被 `export *` 自动重新导出。

默认导出需要显式处理：

```js
export {
  default as createLogger
} from "./logger.js";
```

#### (3)、Barrel 文件

下面这种聚合导出的文件经常叫 barrel：

```js
// services/index.js
export {
  UserService
} from "./user-service.js";

export {
  OrderService
} from "./order-service.js";

export {
  PaymentService
} from "./payment-service.js";
```

其他文件可以：

```js
import {
  UserService,
  OrderService
} from "./services/index.js";
```

或者根据解析配置：

```js
import {
  UserService,
  OrderService
} from "./services";
```

### 7.7、静态导入与动态导入

#### (1)、静态 `import`

```js
import {
  createClient
} from "./client.js";
```

静态导入具有固定语法结构，它不能直接写在普通条件语句中：

```js
if (condition) {
  import {
    createClient
  } from "./client.js";
}
```

这不是合法的静态导入写法，静态导入通常必须位于模块顶层。

#### (2)、动态 `import()`

动态导入是一个表达式，它返回 Promise。

```js
const module = await import("./client.js");
```

导入命名导出：

```js
const module = await import("./math.js");

module.add(2, 3);
```

也可以解构：

```js
const {
  add
} = await import("./math.js");
```

导入默认导出：

```js
const {
  default: createLogger
} = await import("./logger.js");
```

#### (3)、条件加载

```js
if (config.enableAnalytics) {
  const {
    initializeAnalytics
  } = await import("./analytics.js");

  initializeAnalytics();
}
```

只有条件成立时才加载。例如：

```js
async function loadDatabase(driver) {
  if (driver === "postgres") {
    return import("./postgres-driver.js");
  }

  if (driver === "mysql") {
    return import("./mysql-driver.js");
  }

  throw new Error(`Unsupported driver: ${driver}`);
}
```

### 7.8、package.json

`package.json` 可以理解为一个前端项目的“身份证 + 依赖清单 + 命令入口 + 工具配置”。

npm、pnpm、Yarn、Node.js、Vite、Webpack，以及各种工程化工具，都会读取它。它必须是严格的 JSON：不能写注释、不能有尾逗号、属性名必须使用双引号。npm 官方完整字段说明可参考 [package.json 文档](https://docs.npmjs.com/cli/v11/configuring-npm/package-json/)。

下面按照实际前端项目中的重要程度讲解。

#### (1)、一个典型的前端项目配置

以 Vue 3 + Vite + TypeScript 项目为例：

```json
{
  "name": "my-vue-app",
  "version": "1.0.0",
  "private": true,
  "description": "一个基于 Vue 3 和 Vite 的后台管理系统",
  "type": "module",

  "scripts": {
    "dev": "vite",
    "build": "vue-tsc -b && vite build",
    "preview": "vite preview",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "test": "vitest run",
    "test:watch": "vitest",
    "type-check": "vue-tsc --noEmit"
  },

  "dependencies": {
    "axios": "^1.7.0",
    "pinia": "^2.2.0",
    "vue": "^3.5.0",
    "vue-router": "^4.4.0"
  },

  "devDependencies": {
    "@vitejs/plugin-vue": "^5.1.0",
    "@vue/tsconfig": "^0.5.0",
    "eslint": "^9.0.0",
    "typescript": "^5.6.0",
    "vite": "^5.4.0",
    "vitest": "^2.0.0",
    "vue-tsc": "^2.1.0"
  },

  "engines": {
    "node": ">=20.0.0",
    "npm": ">=10.0.0"
  },

  "packageManager": "pnpm@9.12.0"
}
```

实际项目不一定包含所有字段，但其中最常见的是：

* `name`
* `version`
* `private`
* `scripts`
* `dependencies`
* `devDependencies`



#### (2)、项目基本信息

##### 1. `name`

项目或 npm 包的名称：

```json
{
  "name": "my-admin-system"
}
```

如果准备发布到 npm，它必须遵守 npm 包命名规则，一般使用小写字母和连字符。

带作用域的包名：

```json
{
  "name": "@my-company/ui-components"
}
```

这里的 `@my-company` 是组织或作用域名称。

对于只在公司内部开发、不发布到 npm 的普通前端应用，名称主要用于：

* 标识项目；
* 显示在 npm/pnpm 命令输出中；
* Monorepo 工作区引用；
* 生成构建信息。

##### 2. `version`

项目版本：

```json
{
  "version": "1.2.3"
}
```

通常遵循语义化版本，即：

```text
主版本.次版本.修订版本
 MAJOR.MINOR.PATCH
```

例如：

* `1.0.0`：第一个正式版本；
* `1.0.1`：修复 Bug；
* `1.1.0`：增加向后兼容的新功能；
* `2.0.0`：出现不兼容的重大变化；
* `2.0.0-beta.1`：测试版本。

如果需要发布 npm 包，`name` 和 `version` 是最重要的标识字段，版本必须满足语义化版本格式。[npm 官方说明](https://docs.npmjs.com/cli/v11/configuring-npm/package-json/)​

##### 3. `private`

```json
{
  "private": true
}
```

表示这是一个私有项目，不允许执行 `npm publish` 发布到 npm 公共仓库。

普通业务前端项目建议添加：

```json
"private": true
```

它可以避免开发人员误发布公司项目。

注意：这里的“私有”不代表代码会自动加密，也不代表别人无法访问代码；它只是阻止 npm 发布。

##### 4. `description`

```json
{
  "description": "企业内部订单管理系统前端"
}
```

用于描述项目功能。发布 npm 包时，它也会显示在 npm 搜索结果中。

##### 5. `keywords`

```json
{
  "keywords": [
    "vue",
    "admin",
    "dashboard",
    "typescript"
  ]
}
```

主要用于 npm 包搜索。普通业务项目可以不写。

##### 6. `author`

```json
{
  "author": "Zhang San <zhangsan@example.com>"
}
```

也可以使用对象：

```json
{
  "author": {
    "name": "Zhang San",
    "email": "zhangsan@example.com",
    "url": "https://example.com"
  }
}
```

团队项目有时会使用：

```json
{
  "contributors": [
    {
      "name": "Zhang San"
    },
    {
      "name": "Li Si"
    }
  ]
}
```

##### 7. `license`

```json
{
  "license": "MIT"
}
```

常见许可证：

* `MIT`
* `Apache-2.0`
* `GPL-3.0`
* `ISC`
* `UNLICENSED`

公司内部、不允许公开使用的项目可以写：

```json
{
  "license": "UNLICENSED",
  "private": true
}
```



#### (3)、`scripts`：项目命令入口

`scripts` 用来定义项目可执行命令：

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "test": "vitest run",
    "lint": "eslint ."
  }
}
```

执行方式：

```bash
npm run dev
npm run build
npm run lint
```

或者使用 pnpm：

```bash
pnpm dev
pnpm build
pnpm lint
```

npm 会自动把 `node_modules/.bin` 添加到脚本的命令搜索路径，所以可以直接写：

```json
"dev": "vite"
```

不需要写：

```json
"dev": "./node_modules/.bin/vite"
```

npm 支持任意自定义脚本，以及 `pre`、`post` 前后置脚本。[npm Scripts 文档](https://docs.npmjs.com/cli/using-npm/scripts/)​



常见前端脚本

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "build:test": "vite build --mode test",
    "build:prod": "vite build --mode production",
    "preview": "vite preview",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "format": "prettier --write .",
    "type-check": "tsc --noEmit",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "test:e2e": "playwright test"
  }
}
```

这里的冒号没有特殊语法意义，只是一种命名习惯：

```text
build:test
build:prod
lint:fix
test:e2e
```

让相关命令看起来更有层次。



生命周期脚本

例如：

```json
{
  "scripts": {
    "prebuild": "npm run lint",
    "build": "vite build",
    "postbuild": "node scripts/report-build.js"
  }
}
```

执行：

```bash
npm run build
```

npm 会按照下面的顺序执行：

```text
prebuild → build → postbuild
```

需要谨慎使用 `preinstall`、`install` 和 `postinstall`，因为它们会在安装依赖时自动运行，可能造成：

* 安装速度变慢；
* 跨平台兼容问题；
* CI 构建失败；
* 潜在供应链安全风险。



#### (4)、`dependencies`：生产依赖

```json
{
  "dependencies": {
    "axios": "^1.7.0",
    "vue": "^3.5.0",
    "vue-router": "^4.4.0"
  }
}
```

这里通常放应用运行时需要的包，例如：

* Vue、React；
* Vue Router、React Router；
* Axios；
* Pinia、Redux；
* 日期处理库；
* UI 组件库；
* 表单验证库。

安装生产依赖：

```bash
npm install axios
```

或者：

```bash
pnpm add axios
```

包管理器会自动更新 `package.json`，通常不建议手工添加版本号。

判断标准是：

> 删除这个依赖后，最终运行的应用是否会缺失必要功能？

如果会，就通常应该放到 `dependencies`。



#### (5)、`devDependencies`：开发依赖

```json
{
  "devDependencies": {
    "eslint": "^9.0.0",
    "prettier": "^3.3.0",
    "typescript": "^5.6.0",
    "vite": "^5.4.0",
    "vitest": "^2.0.0"
  }
}
```

这里放只在开发、编译、测试阶段使用的工具，例如：

* Vite、Webpack；
* TypeScript；
* ESLint；
* Prettier；
* Vitest、Jest；
* Playwright；
* Babel；
* 各种编译插件；
* 类型声明包。

安装开发依赖：

```bash
npm install eslint --save-dev
```

简写：

```bash
npm install eslint -D
```

pnpm 对应：

```bash
pnpm add eslint -D
```

npm 官方的基本定义是：

* `dependencies`：应用生产运行需要；
* `devDependencies`：本地开发和测试需要。

详见 [npm 依赖分类说明](https://docs.npmjs.com/specifying-dependencies-and-devdependencies-in-a-package-json-file/)。



一个容易误解的地方

对于 Vite 构建的纯前端应用，`vue`、`axios` 最终也会被打包进静态资源，并不会原样保留在服务器的 `node_modules` 中。

但它们仍然属于应用的功能依赖，通常放在：

```json
"dependencies"
```

而 Vite、ESLint、TypeScript 属于构建工具，放在：

```json
"devDependencies"
```



#### (6)、依赖版本符号

例如：

```json
{
  "dependencies": {
    "vue": "^3.5.0",
    "axios": "~1.7.2",
    "dayjs": "1.11.13"
  }
}
```



精确版本

```json
"dayjs": "1.11.13"
```

只接受这个版本。

优点是结果更可控；缺点是不会自动获得修订版本更新。

`​`

`^`：兼容的次版本和修订版本

```json
"vue": "^3.5.0"
```

对于正常的 `1.0.0` 以上版本，大致相当于：

```text
>=3.5.0 且 <4.0.0
```

可以升级：

```text
3.5.1
3.6.0
3.9.9
```

不会升级到：

```text
4.0.0
```

`​`

`~`：通常只允许修订版本变化

```json
"axios": "~1.7.2"
```

大致相当于：

```text
>=1.7.2 且 <1.8.0
```

可以升级：

```text
1.7.3
1.7.9
```

不能升级到：

```text
1.8.0
```

`​`

`*` 或 `latest`

```json
"some-package": "*"
```

或者安装时使用：

```bash
npm install some-package@latest
```

不建议在正式项目中把依赖写成 `*`，因为每次安装可能得到差异很大的版本。



版本范围不等于实际安装版本

假设 `package.json` 中写的是：

```json
"axios": "^1.7.0"
```

它表示“允许安装的版本范围”，而 `package-lock.json`、`pnpm-lock.yaml` 或 `yarn.lock` 记录实际解析出来的版本。

因此：

* `package.json`：声明项目需要什么；
* 锁文件：记录这一次具体安装了什么。

团队项目通常应该提交锁文件。



#### (7)、`type`：模块类型

```json
{
  "type": "module"
}
```

它主要影响 Node.js 如何解释 `.js` 文件。



ES Module

```json
{
  "type": "module"
}
```

此时 `.js` 文件默认使用 ESM：

```js
import fs from "node:fs";

export function readFile() {}
```



CommonJS

```json
{
  "type": "commonjs"
}
```

或者不写 `type`，Node.js 环境中通常会把 `.js` 按 CommonJS 处理：

```js
const fs = require("node:fs");

module.exports = {};
```

现代 Vite 前端项目通常使用：

```json
"type": "module"
```

注意，它不仅影响业务代码，还可能影响：

* `vite.config.js`
* `eslint.config.js`
* Node.js 构建脚本
* 测试配置文件

另外：

* `.mjs` 明确表示 ES Module；
* `.cjs` 明确表示 CommonJS。



#### (8)、Node 和包管理器版本

`engines`

```json
{
  "engines": {
    "node": ">=20.0.0",
    "npm": ">=10.0.0"
  }
}
```

表示项目期望使用的运行环境版本。

还可以限制版本区间：

```json
{
  "engines": {
    "node": ">=20.19.0 <23"
  }
}
```

需要注意：`engines` 在很多情况下主要起提示和约束声明作用，不一定会默认阻止安装；具体是否严格失败还受包管理器配置影响。



`packageManager`

```json
{
  "packageManager": "pnpm@9.12.0"
}
```

用于说明项目应该使用什么包管理器及其版本。

常见写法：

```json
"packageManager": "npm@10.8.2"
```

```json
"packageManager": "pnpm@9.12.0"
```

```json
"packageManager": "yarn@4.5.0"
```

它可以减少团队成员混用 npm、pnpm 和 Yarn 导致的锁文件冲突。

建议一个项目只保留一种锁文件：

```text
npm   → package-lock.json
pnpm  → pnpm-lock.yaml
Yarn  → yarn.lock
```

不要同时提交三种锁文件。



## 八、异步 JavaScript

### 8.1、Promise

#### (1)、Promise 表示未来结果

```js
const promise = fetchUser();
```

`promise` 不是最终用户数据，而是一个代表未来结果的对象。

Promise 有三种状态：

```text
pending    等待中
fulfilled  已成功
rejected   已失败
```

状态转换只能发生一次：

```text
pending → fulfilled
pending → rejected
```

完成后不能再次改变。

#### (2)、Promise executor 同步执行

`new Promise` 接收的函数通常称为 executor。

```js
console.log("A");

const promise = new Promise(resolve => {
  console.log("B");
  resolve("done");
});

console.log("C");
```

输出：

```text
A
B
C
```

executor 在创建 Promise 时立即同步执行。

异步的是之后注册的 Promise 处理函数：

```js
promise.then(value => {
  console.log(value);
});
```

### 8.2、`async` 函数

#### (1)、`async` 函数总是返回 Promise

```js
async function getValue() {
  return 42;
}

// result 是 Promise，不是数字 42
const result = getValue();


```

近似相当于：

```js
function getValue() {
  return Promise.resolve(42);
}
```

读取结果：

```js
getValue().then(value => {
  console.log(value);
});
```

或者：

```js
const value = await getValue();
```

### 8.3、`await`

#### (1)、`await` 等待 Promise 的结果

```js
async function loadUser() {
  const user = await fetchUser();
  return user;
}
```

可以近似理解为：

```js
function loadUser() {
  return fetchUser().then(user => {
    return user;
  });
}
```

但 `async/await` 通常更接近同步代码的阅读方式。




















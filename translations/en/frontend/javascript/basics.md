---
translation_id: javascript-basics
description: "JavaScript dynamic typing, scope, functions, prototypes, modules, and asynchronous programming."
---

# JavaScript Fundamentals

## 1. The JavaScript runtime

### 1.1 Dynamic typing

In JavaScript, “dynamic typing” means that the type of the **variable itself is not fixed. Instead, the type is determined by the value that the variable currently holds at runtime.**

```js
let value = 10;       // The current value is "number".
value = "hello";       // The value is now a string.
value = true;         // The value is now a boolean.
```

A variable can hold values of different types over time. Use `typeof` to inspect a value at runtime:

```js
console.log(typeof 10);      // "number"
console.log(typeof "hello");  // "string"
console.log(typeof true);    // "boolean"
```

It should be noted that “dynamic type” does not mean “no type”. In JavaScript, values like **still have a specific type, such as**. For example, `number`, `string`, `boolean`, `object`, etc. are all specific types. It’s just that there isn’t a permanent binding between variables and types.

It’s very flexible, but it can also lead to errors being exposed only during runtime.

```js
function add(a, b) {
  return a + b;
}

add(1, 2);     // 3
add("1", 2);   // “12”, because of the type conversion that occurred.
```

Therefore, TypeScript is commonly used in actual development to add static type checking on top of JavaScript.



### 1.2 The eight JavaScript value types

There are seven basic types in JavaScript, along with one object type.

* Basic types: undefined, null, boolean, number, bigint, string, symbol
* Object type: object

The types of the following objects are all object:

```js
{}
[]
new Date()

new Map()
new Set()
```

However, the function is a bit special:

```js
typeof function test() {} // "function"
```

In terms of the language model, the function still belongs to the object. However, `typeof` is specifically used to return `"function"` for the function.

Common `typeof` results:

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

A legacy issue from the past: the value returned by typeof null is "object". This doesn’t mean that `null` is actually an object. It’s a behavior that remained from the early design of JavaScript.

Therefore, to determine whether `null` is null, you can simply write: value === null.

To determine whether a value is an array, use: `Array.isArray(value)`. Do not use `typeof value === "array"`, as this condition will never be true.



(1) The difference between undefined and null

Among them, both undefined and null can represent “no value”, but their semantics are different.

undefined: Usually means "not provided" or "not yet assigned". Refer specifically to the following examples of codes:

```js
let result;
console.log(result); // undefined

function greet(name) {
  console.log(name);
}

greet(); // undefined
```

null: Usually, it is an empty value set by the developer voluntarily.

```js
const selectedUser = null;
```

In summary, it can be understood as follows:

* undefined: There is no value here, or value is not provided.
* null: This is explicitly set to null.



### 1.3 `const` and `let`

Both `const` and `let` are used to state variables, the core difference being whether the **variable can be revalued**.

```js
let age = 18;
age = 19; // Yeah.

const name = "小明";
name = "小红"; // Wrong report: cannot revalue
```

However, the object or array denoted by `const` can still have its **content modified**.

```js
const user = { name: "小明" };
user.name = "小红"; // Yeah.

const numbers = [1, 2];
numbers.push(3); // Yeah.
```

Do not replace the entire variable with another object or array:

```js
user = { name: "小刚" }; // Wrong report.
numbers = [4, 5];        // Wrong report.
```

Simple comprehension:

* `let`: Used when re-valued after variable.
* `const`: The variable is used when it is not revalued.

Priority is usually given to `const` and `let` is used when determining the need for re-allocation.

There are also some commonalities between the two:

* All are block-level scopes.
* Neither of them can be declared repeatedly within the same scope.
* Any access before the declaration will result in an error.
* `const` The declaration must be given immediate value:

```js
let value;    // Yeah.
const value;  // Wrong report.
```



### 1.4 Strict and loose equality

Core distinction:

* `==`: It’s a loose equality comparison. The types may be automatically converted before the comparison.
* `===`: Exact equality. No type conversion is performed. Both the type and the value are compared.

```js
5 == "5"   // true. The string "5" is converted into a number.
5 === "5"  // False, different types.
```

More examples:

```js
0 == false        // true
0 === false       // false

"" == false       // true
"" === false      // false

null == undefined   // true
null === undefined  // false
```

The comparison between objects and arrays is based on whether the references are the same:

```js
[1, 2] === [1, 2] // False. Two different array objects.

const a = [1, 2];
const b = a;

a === b // true, pointing to the same array.
```

In actual development, it is recommended to use `===` and `!==` by default. This makes the results clearer and helps avoid unexpected situations caused by implicit type conversions.

```js
if (age === 18) {
  // ...
}
```

Only use `==` when it is indeed necessary to have relaxed comparison rules and when the result of type conversion is clear.



## 2. Scope and Closures

### 2.1 What is scope?

The scope determines where a variable can be accessed.

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

Here:

* `appName` is located in the outer field, and the internal function can access it.
* `version` The function external cannot access the funnel shop located at `start`.

It can be painted as:

```text
Global scope
├── appName
└── start
    └── Function scope
        └── version
```

When JavaScript looks for a variable, it starts looking from the current position to the outward layer:

```text
Current scope → enclosing scope → further enclosing scopes → global scope
```

This lookup relationship is called the **scope chain**.



Common scopes in JavaScript

* In the global scope, declared at the outermost layer of a regular script:

```js
const appName = "My App";
```

In real projects, modules are typically used. Therefore, each module has its own top-level scope, preventing all variables from actually entering the global environment.

* The scope of a function, parameters of a function, and variables declared within the function belong to the function itself:

```js
function calculate(price, count) {
  const total = price * count;
  return total;
}
```

Here, `price`, `count` and `total` can only be accessed within `calculate`.

* Block shop, formed by a pair of brackets, for example:

```js
if (true) {
  const message = "hello";
  let count = 1;
}

// The variables `message` and `count` are not accessible here.
```



(2) Variable masking

Inner scopes can declare variables with the same name as those in the outer scope:

```js
const config = "global config";

function initialize() {
  const config = "local config";
  console.log(config);
}

initialize();
console.log(config);
```

Output:

```text
local config
global config
```

function `config` covers the outer layer `config`. This is called variable masking, or shadowing.



(3) The scope differences of `var`, `let`, and `const`

Modern projects mainly use `const` and `let` but `var` may still appear in old projects, compile output and depend on codes.

`let` and `const` are block-level scopes.

```js
if (true) {
  let count = 1;
  const name = "Alice";
}

// You cannot access the `count` and `name` variables here.
```

`var` is function shop

```js
function test() {
  if (true) {
    var count = 1;
  }

  console.log(count);
}

test();
```

The output result is: 1

The brackets of `if` do not limit `var`. In this example, `count` belongs to the entire `test` function.

If it is not surrounded by a function:

```js
if (true) {
  var value = 10;
}

console.log(value); // 10
```

This is also why modern code usually avoids using `var`: its scope boundaries are not intuitive enough.



### 2.2. Variable Hoisting

JavaScript deals with declarations in a field before it is implemented.

Therefore, some declarations can be used before they appear in the code. This phenomenon is commonly referred to as **hoisting**.

However, the improvement behaviors of different declarations are different.

(1) The promotion of function declarations

When using function declarations, you can call the function before declaring it:

```js
greet();

function greet() {
  console.log("hello");
}
```

You can roughly think of it as follows: When the scope is entered, JavaScript has already created the `greet` function.

This behavior is often used to place the main logic above the file, while placing the auxiliary functions below the file:

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

Even if the helper functions are written later, the `processData` in front can still call them.

(2) Function expressions do not work the same way as function declarations.

The following code will cause an error:

```js
greet();

const greet = function () {
  console.log("hello");
};
```

The same applies to arrow functions:

```js
greet();

const greet = () => {
  console.log("hello");
};
```

Since what is being upgraded here is the variable declaration, rather than assigning function values to variables in advance.

The essence of these two writings is:

```js
const greet = 某个函数值;
```

Only after the assignment statement is executed does `greet` actually store the value.

So, it should be written as:

```js
const greet = () => {
  console.log("hello");
};

greet();
```



### 2.3 What is a closure?

Let’s look at an example where a function returns another function:

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

According to common intuition, `createCounter()` has already been executed, and its local variable `count` should also disappear.

However, the returned `increment` function still references `count`. Therefore, `count` will continue to exist.

This is what a closure is: a function plus the outer lexical environment that it has access to when defining that function.

It can be imagined as follows:

```text
counter
  │
  ▼
increment function
  │
  └── Refers to count in the scope of createCounter
```

As long as `counter` is still accessible, this closure and the outer variable it needs can still be accessed.

(1) Each function call generates a new lexical environment.

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

`first` and `second` do not share `count`.

Since `createCounter()` is called twice, a new local environment will be created each time.

```text
first  → count: 2
second → count: 1
```

In other words, each call results in a separate state.

(2) The classic closure problem of `var` in the loop

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

The output is 3, 3, 3.

The reason is:

* `var` is function shop, not black shop.
* The three functions that reference the same `i` are all closures.
* After the loop ends, this `i` has been replaced by `3`.
* When the functions are called, they read the current value of `i`, not the snapshot taken when the functions were created.

Use `let`:

```js
const functions = [];

for (let i = 0; i < 3; i++) {
  functions.push(function () {
    console.log(i);
  });
}
```

The output is: 0, 1, 2

When using `let` in the loop within `for`, JavaScript will create a binding for the loop variable for each iteration.



## 3. Functions

### 3.1. How to create functions

(1) Function Declaration

```js
function add(a, b) {
  return a + b;
}
```

(2) Function Expressions

```js
const add = function (a, b) {
  return a + b;
};
```

First, a function value is created, and then it is assigned to the variable `add`.

Since `add` is a variable of type `const`, it cannot be called before being assigned to anything.

```js
add(2, 3); // ReferenceError

const add = function (a, b) {
  return a + b;
};
```

(3) Arrow functions

```js
const add = (a, b) => {
  return a + b;
};
```

If the function body consists of only one expression, the curly braces and `return` can be omitted.

```js
const add = (a, b) => a + b;
```

When there is only one parameter, the parameter parentheses can be omitted:

```js
const double = value => value * 2;
```

Where no parameters or multiple parameters are available, brackets must be retained:

```js
const getTime = () => Date.now();

const add = (a, b) => a + b;
```



### 3.2 Rest parameters with `...args`

The remaining parameters can be collected into an array for convenience:

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

`numbers` is a true array:

```js
Array.isArray(numbers) // true
```

The remaining parameters can also be used together with regular parameters:

```js
function log(level, ...messages) {
  console.log(level, messages);
}

log("info", "Server started", "Port:", 3000);
```

The parameters received for `level` and `messages` are as follows:

```text
level    → "info"
messages → ["Server started", "Port:", 3000]
```

The remaining parameters must be the last parameter.



### 3.3 Return values

```js
function greet() {
  console.log("Hello");
}

const result = greet();

console.log(result); // undefined
```



### 3.4. Callback functions

The function passed as a parameter to another function is usually called a callback function.

```js
function execute(callback) {
  callback();
}

execute(() => {
  console.log("Executed");
});
```

`execute` is the receiving function, anrow operation is a callback.



## 4. How `this` is bound

`this` is one of the most misunderstood mechanisms in JavaScript.

Remember one important point: the `this` keyword in regular functions is usually determined by the way the function is called. In contrast, the `this` in arrow functions is determined by the location where the function is defined.

### 4.1. The `this` keyword for regular functions

Consider an object:

```js
const user = {
  name: "Alice",

  introduce() {
    console.log(this.name);
  }
};

user.introduce(); // "Alice"
```

The call point is located to the left of `user`. Therefore, in this call:

```js
this === user
```

It can be approximated as follows:

```js
introduce.call(user);
```

However, the `introduce` function does not permanently belong to `user`.

```js
const anotherUser = {
  name: "Bob",
  introduce: user.introduce
};

anotherUser.introduce(); // "Bob"
```

When the same function is called by different objects, the value of this also changes.

```text
user.introduce()        → this is user
anotherUser.introduce() → this is anotherUser
```

### 4.2. The `this` keyword in arrow functions

The most important sentence in an arrow function is:

> Arrow functions do not have their own `this`. Instead, they use the `this` from the outer scope in which they are defined.

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

fn(); // Xiao Ming
```

The execution process is as follows:

1. Call `user.createArrow()`
2. `createArrow` is a regular function, so its `this` is `user`.
3. When the arrow function is created, the `this` in `createArrow` is captured.
4. Even if `fn()` is executed separately later on, it still uses the previously captured `user`.



(1) Pitfalls in using arrow functions in object methods

```js
const user = {
  name: "小明",

  sayName: () => {
    console.log(this.name);
  }
};

user.sayName();
```

The object literal `{}` does not create a new `this` scope. This arrow function will capture the `this` outside of the object, rather than the `user`.

It can be approximated as follows:

```js
const outerThis = this;

const user = {
  name: "小明",

  sayName: () => {
    console.log(outerThis.name);
  }
};
```

The correct way to write it is to use the regular method:

```js
const user = {
  name: "小明",

  sayName() {
    console.log(this.name);
  }
};

user.sayName(); // Xiao Ming
```

Or:

```js
const user = {
  name: "小明",

  sayName: function () {
    console.log(this.name);
  }
};
```



(2) Arrow functions are suitable for nested callbacks.

One of the important issues that arrow functions initially addressed was that callback functions would lose the outer `this` context.

For issues related to regular function callbacks, please refer to the following code:

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

When `user.introduce()` is called, `this` in `introduce` is equal to `user`.

However, the function passed to `setTimeout` is another ordinary function. When it is called by a timer, it doesn’t go through:

```js
user.someFunction();
```

The call is made, so its `this` is no longer `user`.

However, using arrow functions can solve this problem:

```js
const user = {
  name: "小明",

  introduce() {
    setTimeout(() => {
      console.log(this.name);
    }, 1000);
  }
};

user.introduce(); // Output “Xiao Ming” after 1 second.
```

Here:

1. `introduce` is a regular method.
2. `user.introduce()` Make `this` in `introduce` `user`
3. The timer arrow function captures `this` from `introduce`.
4. Therefore, `user` can still be accessed during the callback.

In the past, when arrow functions weren’t available, this was often written like this:

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



## 5. Prototypes, prototype chains, and classes

JavaScript is a “prototype-based” language. Even when using `class`, the underlying mechanism still primarily relies on prototypes and the prototype chain to achieve property sharing, method reuse, and inheritance.

Summarize it in one sentence:

> Each ordinary object can be associated with another object as its prototype. When accessing an object’s properties, if the property does not exist within the object itself, JavaScript will continue searching along the prototype chain until the property is found or it reaches `null`. This search path is known as the prototype chain.

### 5.1. What is a prototype?

Each ordinary object usually has an internal prototype link.

```js
const user = {
  name: "Alice"
};
```

It can be approximated as:

```text
user
├── Own property: name
└── [[Prototype]] ──→ Object.prototype
                         ├── toString
                         ├── valueOf
                         ├── hasOwnProperty
                         └── ...
```

`[[Prototype]]` is the internal concept used in the norm and not the attribute name used directly by the ordinary code.

Through:

```js
Object.getPrototypeOf(user)
```

Reading the prototype of the object:

```js
Object.getPrototypeOf(user) === Object.prototype
// true
```

#### (1) The process of finding attributes

When executed:

```js
user.name
```

JavaScript will:

1. Check whether `user` itself contains `name`.
2. Return directly to `"Alice"` when found

When executed:

```js
user.toString
```

JavaScript will:

1. Check whether `user` itself contains `toString`.
2. No such item was found.
3. Go to the prototype of `user`
4. Find `toString` in `Object.prototype`.
5. Return this function.

This is the prototype chain attribute search.

If there is no such prototype currently, continue searching upwards until you encounter:

```js
null
```

The complete path is roughly as follows:

```text
Current object
   ↓
Prototype of the current object
   ↓
Next prototype
   ↓
...
   ↓
null
```

If `null` is still not found after reaching it, then return:

```js
undefined
```



#### (2) The difference between `in` and `Object.hasOwn()`

Please first look at the following sample code:

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

* Use `in` to check: the object itself and the entire prototype chain.
* Use `Object.hasOwn()` to check only the object itself.

#### (3) Attribute masking

Objects can define their own properties with the same name as the prototype properties:

```js
const user = {
  name: "Alice",

  toString() {
    return this.name;
  }
};

user.toString(); // "Alice"
```

When searching for `toString`:

1. Find it on your own at `user`
2. Do not continue searching `Object.prototype.toString`

It's called attribute cover.

If the attribute itself is deleted:

```js
delete user.toString;
```

Access again:

```js
user.toString
```

The version on the prototype will be found.

#### (4) How to obtain the prototype of an object?

Recommended for use:

```js
Object.getPrototypeOf(user);
```

For example:

```js
const user = {};

console.log(
  Object.getPrototypeOf(user) === Object.prototype
); // true
```

It can also be done through:

```js
user.__proto__
```

Read it, but `__proto__` is a legacy access method and is not recommended to be used in official code.

Recommended for writing:

```js
Object.getPrototypeOf(obj);
Object.setPrototypeOf(obj, prototype);
```

However, frequent use of `Object.setPrototypeOf()` to modify the prototype of existing objects may affect JavaScript engine optimization. When designing object structures, it is usually necessary to determine the prototype during the creation phase.



### 5.2. Manually creating prototype relationships

#### (1), `Object.create`

**`Object.create()`** functions as **to create a new object and point the new object `__proto__` (internal prototype pointer) to the transferred parameter object**.

See the code below:

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

Prototype relationships:

```text
dog
├── name
├── bark
└── [[Prototype]] ──→ animal
                       └── breathe
```



### 5.3, Prototype Chain

#### (1) Multi-layer prototype chain

For more details, see the code below:

```js
function User(name) {
  this.name = name;
}

User.prototype.introduce = function () {
  console.log(this.name);
};

const alice = new User("Alice");
```

The prototype chain is roughly as follows:

```text
alice
  ↓ [[Prototype]]
User.prototype
  ↓ [[Prototype]]
Object.prototype
  ↓ [[Prototype]]
null
```

Reading: alice.name, found at `alice`.

Reading: alice.introduce, found at `User.prototype`.

Reading: alice.toString, in:

```text
alice             not found
User.prototype    not found
Object.prototype  found
```

#### (2) The array’s prototype chain

```js
const items = [1, 2, 3];
```

`items` did not save a copy of `map`:

```js
Object.hasOwn(items, "map"); // false
```

However, you can call it like this:

```js
items.map(item => item * 2);
```

Because the prototype chain is roughly like this:

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

Verify:

```js
Object.getPrototypeOf(items) === Array.prototype
  // true
```

This explains why all arrays can share array methods, without the need for each array to store a separate `map`.

#### (3) The prototype chain of the function

```js
function greet() {
}
```

`greet` is itself a function object, so:

```js
Object.getPrototypeOf(greet) === Function.prototype
   // true
```

This is why it can be called:

```js
greet.call(...)
greet.apply(...)
greet.bind(...)
```

Because these methods usually come from:

```js
Function.prototype
```

The relationship is roughly as follows:

```text
greet function object
  ↓
Function.prototype
  ↓
Object.prototype
  ↓
null
```

#### (4) The instanceof check for the prototype chain

```js
class Animal {
}

class Dog extends Animal {
}

const dog = new Dog();
```

Results:

```js
dog instanceof Dog;    // true
dog instanceof Animal; // true
dog instanceof Object; // true
```

The core issue with `instanceof` is: does the prototype of the constructor appear in the prototype chain of the object?

For example: dog instanceof Animal

Approximate check: Does Animal.prototype exist in the prototype chain of dog?

Because:

```text
dog
↓
Dog.prototype
↓
Animal.prototype
```

So the result is `true`.



### 5.4, class

#### (1) Basic class definitions

See the sample code below:

```js
class User {
  //
负责初始化实例自身属性
  constructor(name) {
    this.name = name;
  }

  //The introduce function will be defined as follows: User.prototype
  introduce() {
    console.log(`I am ${this.name}`);
  }
}

const alice = new User("Alice");

alice.introduce();
```

It can be verified as follows:

```js
Object.hasOwn(alice, "name"); // true

Object.hasOwn(alice, "introduce"); // false

Object.hasOwn(User.prototype, "introduce"); // true
```

So:

```js
alice.introduce === User.prototype.introduce
  // true
```



#### (2), extends

For more details, please refer to the code below:

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

`Dog` does not define `introduce` and `move`, but examples can be found through prototype plan.

The prototype relationships are roughly as follows:

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

#### (3) Subclass constructors and super()

```js
class Dog extends Animal {
  constructor(name, breed) {
    super(name);
    this.breed = breed;
  }
}
```

Subcategory constructor must call before using `this`:

```js
super(...)
```

`super(name)` Calls the parent class constructor and initializes the current instance using the parent class.

Note that it does not create a separate instance of `Animal` and then insert it into `Dog`.

`Dog` There are still only one examples:

```text
Same dog instance
├── name initialized by the Animal constructor
└── breed initialized by the Dog constructor
```

#### (4) Getters and Setters

An example of a getter function is as follows:

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

The access form appears to be `property: rectangle.area`, but in reality, it is a getter function that is called.

Do not write it as: rectangle.area(). The Getter is suitable for calculating derived properties.



An example of the setter function is as follows:

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

Assigning values: user.name = "Bob"; will call the setter function.

Reading: user.name will trigger a getter method.

`_name` just name deal, not really private.



## 6. Arrays, collections, iterators

### 6.1 Array basics

```js
const users = ["Alice", "Bob", "Charlie"];

// Arrays access its elements through numerical indices:
users[0]; // "Alice"
users[1]; // "Bob"
users[2]; // "Charlie"

// Arrays are also objects:
typeof users // "object"

// To determine whether a value is an array, use Array.isArray.
Array.isArray(users) // true
```

### 6.2 Methods that modify the original array

#### (1) `push` and `pop`

push: Adds an element at the end of the array and returns the new length:

```js
const items = ["a", "b"];
// Note that the `push` method returns the length, not the array itself.
const length = items.push("c");

console.log(items);  // ["a", "b", "c"]
console.log(length); // 3
```

pop: Removes and returns the last element.

```js
const items = ["a", "b", "c"];

const last = items.pop();

console.log(last);  // "c"
console.log(items); // ["a", "b"]
```

#### (2) `unshift` and `shift`

unshift: Adds an element at the beginning of the array.

```js
const items = ["b", "c"];

items.unshift("a");

console.log(items); // ["a", "b", "c"]
```

shift: Remove and return the first element.

```js
const items = ["a", "b", "c"];

const first = items.shift();

console.log(first); // "a"
console.log(items); // ["b", "c"]
```

Since other elements at the beginning usually require reindexing, using `shift` and `unshift` frequently to handle large arrays may be more costly than operating at the end.

#### (3), `splice`

`splice` Elements may be removed, inserted or replaced and the original array may be modified.

```js
array.splice(startIndex, deleteCount, ...newItems)
```

Delete:

```js
const items = ["a", "b", "c", "d"];

const removed = items.splice(1, 2);

console.log(removed); // ["b", "c"]
console.log(items);   // ["a", "d"]
```

Insert:

```js
const items = ["a", "d"];

items.splice(1, 0, "b", "c");

console.log(items); // ["a", "b", "c", "d"]
```

Replace:

```js
const items = ["a", "b", "c"];

items.splice(1, 1, "B");

console.log(items); // ["a", "B", "c"]
```

#### (4), `sort`

`sort` will modify the original array:

```js
const numbers = [3, 1, 2];

const result = numbers.sort();

console.log(numbers); // [1, 2, 3]
console.log(result === numbers); // true
```

The numerical sorting should provide a comparison function:

```js
numbers.sort((a, b) => a - b);
```

Ascending order:

```js
(a, b) => a - b
```

Descending:

```js
(a, b) => b - a
```

### 6.3 Methods to Return a New Array

#### (1), `slice`

`slice` Intercepts some elements, returns a new array, does not modify the original array.

```js
const items = ["a", "b", "c", "d"];

const selected = items.slice(1, 3);

console.log(selected); // ["b", "c"]
console.log(items);    // ["a", "b", "c", "d"]
```

The range includes the starting index, but does not include the ending index.

#### (2), `concat`

```js
const first = [1, 2];
const second = [3, 4];

const combined = first.concat(second);

console.log(combined); // [1, 2, 3, 4]
```

You can also use the expansion syntax:

```js
const combined = [
  ...first,
  ...second
];
```

Neither approach would modify the original array.



### 6.4 Array transformations

#### (1), `map`

`map` converts each element into a new value and returns a new array.

```js
const numbers = [1, 2, 3];

const doubled = numbers.map(number => number * 2);

console.log(doubled); // [2, 4, 6]
```

Convert object:

```js
const names = users.map(user => user.name);
```

Conversion structure:

```js
const options = users.map(user => ({
  label: user.name,
  value: user.id
}));
```

The return value of the callback `map` is very important.

```js
// Example of error
const names = users.map(user => {
  user.name;
});

// Since there is no return statement, the result is:
[undefined, undefined, ...]

// Correct example
const names = users.map(user => {
  return user.name;
});
// Or:
const names = users.map(user => user.name);
```

#### (2), `filter`

`filter` Elements that return a true value in the callback are retained as is.

```js
const activeUsers = users.filter(user => user.active);
```

The original array remains unchanged and returns the new array.

Common ways to handle null values for filtering:

```js
const values = [0, 1, null, 2, undefined, 3];

const result = values.filter(Boolean);
// Results
[1, 2, 3]
```

#### (3), `flat`

```js
const nested = [
  [1, 2],
  [3, 4]
];

nested.flat(); // [1, 2, 3, 4]
```

Only one level is expanded by default:

```js
[1, [2, [3]]].flat();
// [1, 2, [3]]
```

Specify the depth:

```js
[1, [2, [3]]].flat(2);
// [1, 2, 3]
```

Full rollout of common writing:

```js
nested.flat(Infinity);
```

However, structures that are very deep or have circular references require careful handling.

#### (4), `flatMap`

`flatMap` is roughly equivalent to first `map`, and then expanding one layer further:

```js
const sentences = [
  "hello world",
  "javascript language"
];

const words = sentences.flatMap(
  sentence => sentence.split(" ")
);
```

Results:

```js
[
  "hello",
  "world",
  "javascript",
  "language"
]
```

Approximate equivalent:

```js
sentences
  .map(sentence => sentence.split(" "))
  .flat();
```

### 6.5, Map

#### (1) The basic methods for `Map`

```js
const map = new Map();
```

Add or update:

```js
map.set("name", "Alice");
map.set("age", 20);
```

Reading:

```js
map.get("name"); // "Alice"
```

Determine whether the key exists:

```js
map.has("name"); // true
```

Delete:

```js
map.delete("name");
```

Clear:

```js
map.clear();
```

Quantity:

```js
map.size
```

### 6.6 Iterators

#### (1) The iterator `next()`

An iterator is an object that has a `next()` method.

Each call returns:

```js
{
  value: 某个值,
  done: 是否结束
}
```

For example:

```js
const iterator = ["a", "b"][Symbol.iterator]();

iterator.next();
// { value: "a", done: false }

iterator.next();
// { value: "b", done: false }

iterator.next();
// { value: undefined, done: true }
```

`for...of` The internal call will be kept to `next()` until:

```js
done === true
```

#### (2), `Symbol.iterator`

An object that has:

```js
object[Symbol.iterator]()
```

And since this method returns an iterator, it is considered an iterable object.

Manual implementation:

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

Now it can be done:

```js
for (const number of range) {
  console.log(number);
}
```

#### (3) Iterable objects and iterators are not exactly the same concept.

* Iterable objects: objects that can create iterators.
* Iterator: Generates results one by one using next().

Arrays are iterable objects:

```js
const array = [1, 2, 3];
```

Call:

```js
array[Symbol.iterator]()
```

Get an iterator.

An iterable object can be traversed multiple times, as a new iterator is created each time.

```js
for (const value of array) {
}

for (const value of array) {
}
```

And a specific iterator is usually stateful and moves forward in a single direction:

```js
const iterator = array[Symbol.iterator]();

iterator.next();
iterator.next();
```

It remembers the current traversal position.



## 7. Modules and project structure

### 7.1. Why are modules necessary?

If all the code is written in one file:

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

As the project grows, the following issues will occur:

* Variable name conflicts occurred.
* The internal implementation is exposed.
* The responsibilities of the files are mixed up.
* The dependency relationships are difficult to understand.
* Testing is difficult.
* It’s unclear what changes will be made to the scope of influence.

The module breaks the program into several files and explicitly defines:

```text
What this file exports
What this file depends on
```

For example:

```text
src/
├── config.js
├── user-service.js
├── user-repository.js
└── index.js
```

Each file has its own module scope.

```js
// config.js
const secret = "internal";

export const config = {
  port: 3000
};
```

Other modules can only access the exported `config`. They cannot directly access the internal `secret`.

### 7.2, ES Modules

ES Modules, abbreviated as ESM, is a standard JavaScript module system that uses `import` and `export`.

Node.js currently supports ESM in a stable manner, while also retaining the CommonJS module system. [Node.js ESM Official Documentation](https://nodejs.org/api/esm.html)

### 7.3 Named exports

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

Import:

```js
// app.js
import {
  add,
  subtract,
  PI
} from "./math.js";

console.log(add(2, 3));
```

The names in the parentheses must correspond to the exported names:

```js
import {
  add
} from "./math.js";
```

The module loading usually fails when the following names do not exist:

```js
import {
  multiply
} from "./math.js";
```

#### (1) Declare first, and then export them uniformly.

The following two writings function in the same way.

Export directly:

```js
export function add(a, b) {
  return a + b;
}

export const PI = 3.14159;
```

Harmonized export:

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

In real projects, the implementation is often defined first, and then exported collectively at the bottom of the file.

#### (2). Rename at Import

```js
import {
  add as addNumbers
} from "./math.js";
```

Here:

```text
Original export name: add
Local name in this file: addNumbers
```

Usage:

```js
addNumbers(2, 3);
```

Often used to resolve naming conflicts:

```js
import {
  create as createUser
} from "./user.js";

import {
  create as createOrder
} from "./order.js";
```

#### (3) Rename on Export

```js
function internalAdd(a, b) {
  return a + b;
}

export {
  internalAdd as add
};
```

What is seen in other files is:

```js
import {
  add
} from "./math.js";
```

Won't see the name `internalAdd`.

### 7.4 Default Export

#### (1), `export default`

A module can have at most one default export:

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

Do not use brackets when importing default export:

```js
import createLogger from "./logger.js";
```

The default import name is determined by the party that imports it.

```js
import makeLogger from "./logger.js";
```

Both `makeLogger` and `createLogger` are acceptable, as the default export does not require the importer to use a fixed local name.

#### (2) Default export and named export can exist simultaneously.

```js
// logger.js
export const LOG_LEVEL = "info";

export function formatMessage(message) {
  return `[LOG] ${message}`;
}

export default function createLogger() {
}
```

Import:

```js
import createLogger, {
  LOG_LEVEL,
  formatMessage
} from "./logger.js";
```

Of which:

```text
createLogger               → default import
LOG_LEVEL, formatMessage   → named imports
```

#### (3) The meaning of curly braces

```js
// Indicates that the default export is to be imported.
import logger from "./logger.js";

// Indicates importing a named export whose name must be "logger".
import {
  logger
} from "./logger.js";
```

The two are completely different.

Assumption:

```js
export default function logger() {
}
```

It can only be imported in this way:

```js
import logger from "./logger.js";
```

### 7.5. Namespace Import

`import * as`

```js
import * as math from "./math.js";
```

Assume that `math.js` is exported as follows:

```js
export function add() {
}

export function subtract() {
}

export const PI = 3.14159;
```

So, it can be:

```js
math.add(2, 3);
math.subtract(5, 2);
console.log(math.PI);
```

`math` is a module namespace object, containing the exports of that module.

This notation is commonly used in tool modules:

```js
import * as path from "node:path";
```

However, namespace objects are not ordinary configuration objects that can be modified at will. The importing party cannot reassign the exported module.

### 7.6. Re-exporting

#### (1) Export directly from another module

```js
// index.js
export {
  createUser,
  deleteUser
} from "./user-service.js";
```

This also completes the process of obtaining exports from user-service.js, and then exporting them to external locations through index.js.

If the current module does not itself need to use `createUser`, import before export is not necessary.

#### (2), `export *`

```js
export * from "./user-service.js";
export * from "./order-service.js";
```

It will re-export the named exports of the target module. However, the default exports are not automatically re-exported by `export *`.

The default export requires explicit processing:

```js
export {
  default as createLogger
} from "./logger.js";
```

#### (3) Barrel files

The following aggregated output file is often referred to as “barrel”.

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

Other files can be:

```js
import {
  UserService,
  OrderService
} from "./services/index.js";
```

Or according to the parsing configuration:

```js
import {
  UserService,
  OrderService
} from "./services";
```

### 7.7 Static and Dynamic Importing

#### (1) Static `import`

```js
import {
  createClient
} from "./client.js";
```

Static imports have a fixed syntax structure, and they cannot be written directly within ordinary conditional statements:

```js
if (condition) {
  import {
    createClient
  } from "./client.js";
}
```

This is not a valid static import syntax. Static imports usually must be located at the top level of the module.

#### (2) Dynamic `import()`

Dynamic import is an expression that returns a Promise.

```js
const module = await import("./client.js");
```

Import named export:

```js
const module = await import("./math.js");

module.add(2, 3);
```

It can also be deconstructed:

```js
const {
  add
} = await import("./math.js");
```

Import default export:

```js
const {
  default: createLogger
} = await import("./logger.js");
```

#### (3) Conditional loading

```js
if (config.enableAnalytics) {
  const {
    initializeAnalytics
  } = await import("./analytics.js");

  initializeAnalytics();
}
```

It is only loaded when the conditions are met. For example:

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

### 7.8 `package.json`

`package.json` can be understood as the “ID + dependency list + command entry + tool configuration” of a front-end project.

npm, pnpm, Yarn, Node.js, Vite, Webpack, and various engineering tools will all read this. It must be in the strict JSON format: no comments allowed, no trailing commas, and attribute names must be enclosed in double quotes. For a complete list of fields in npm, refer to [Documentation for package.json](https://docs.npmjs.com/cli/v11/configuring-npm/package-json/).

This is explained below in terms of the importance of the actual front-end projects.

#### (1) A typical front-end project configuration

Taking a Vue 3 + Vite + TypeScript project as an example:

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

The actual project may not include all fields, but the most common ones are:

* `name`
* `version`
* `private`
* `scripts`
* `dependencies`
* `devDependencies`



#### (2) Basic project information

##### 1. `name`

Name of the project or npm package:

```json
{
  "name": "my-admin-system"
}
```

If you plan to publish the package to npm, it must follow npm's package naming conventions. Typically, lowercase letters and hyphens are used for naming packages.

Namespace package names:

```json
{
  "name": "@my-company/ui-components"
}
```

Here `@my-company` is the name of the organization or domain.

For regular frontend applications that are developed only within the company and not released to npm, the name is mainly used for:

* Identify the item;
* Displays in npm/pnpm command output;
* Reference to the Monorepo workspace;
* Generates construction information.

##### 2. `version`

Project version:

```json
{
  "version": "1.2.3"
}
```

It generally follows a semantic versioning approach, that is:

```text
major version.minor version.patch version
 MAJOR.MINOR.PATCH
```

For example:

* `1.0.0`: The first official version;
* `1.0.1`: Fixing the bug;
* `1.1.0`: Added backward-compatible new features;
* `2.0.0`: Major changes that are incompatible;
* `2.0.0-beta.1`: Test version.

If you want to publish an npm package, `name` and `version` are the most important identifier fields. The version must follow the semantic versioning format. [Official npm description](https://docs.npmjs.com/cli/v11/configuring-npm/package-json/) remains as it is.

##### 3. `private`

```json
{
  "private": true
}
```

This indicates that it is a private project, and the `npm publish` cannot be published to the npm public repository.

It is recommended to add the following to ordinary business front-end projects:

```json
"private": true
```

It can prevent developers from accidentally releasing company projects.

Note: The term “private” here does not mean that the code will be automatically encrypted, nor does it mean that others cannot access the code. It simply prevents npm from publishing the code.

##### 4. `description`

```json
{
  "description": "企业内部订单管理系统前端"
}
```

It describes the functionality of the project. When the npm package is released, it will also be displayed in the npm search results.

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

It is mainly used for npm package searching. It can be omitted for regular business projects.

##### 6. `author`

```json
{
  "author": "Zhang San <zhangsan@example.com>"
}
```

You can also use objects:

```json
{
  "author": {
    "name": "Zhang San",
    "email": "zhangsan@example.com",
    "url": "https://example.com"
  }
}
```

Team projects sometimes use:

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

Common licenses:

* `MIT`
* `Apache-2.0`
* `GPL-3.0`
* `ISC`
* `UNLICENSED`

For projects that are internal to the company and not allowed to be used publicly, you can write:

```json
{
  "license": "UNLICENSED",
  "private": true
}
```



#### (3) `scripts`: Project command entry

`scripts` is used to define the executable command for the project:

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

Means of implementation:

```bash
npm run dev
npm run build
npm run lint
```

Or use pnpm:

```bash
pnpm dev
pnpm build
pnpm lint
```

npm will automatically add the `node_modules/.bin` to the command search path of the script. So you can write it directly:

```json
"dev": "vite"
```

Do not write:

```json
"dev": "./node_modules/.bin/vite"
```

npm supports any custom script, and `pre`, `post` Back and forth scripts.[npm Scripts documentation](https://docs.npmjs.com/cli/using-npm/scripts/)



Common front-end scripts

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

The colon here has no special syntax meaning. It's just a naming habit:

```text
build:test
build:prod
lint:fix
test:e2e
```

Make the relevant commands more hierarchical in appearance.



Lifecycle scripts

For example:

```json
{
  "scripts": {
    "prebuild": "npm run lint",
    "build": "vite build",
    "postbuild": "node scripts/report-build.js"
  }
}
```

Implementation:

```bash
npm run build
```

npm will be executed in the following order:

```text
prebuild → build → postbuild
```

It is necessary to use `preinstall`, `install`, and `postinstall` with caution, as they will be executed automatically during the installation of dependencies, which may lead to the following issues:

* The installation speed is slowing down.
* Cross-platform compatibility issues;
* CI build failed.
* Potential supply chain security risks.



#### (4) `dependencies`: Dependencies for production

```json
{
  "dependencies": {
    "axios": "^1.7.0",
    "vue": "^3.5.0",
    "vue-router": "^4.4.0"
  }
}
```

This is usually the package needed to apply rantime, for example:

* Vue, React;
* Vue Router, React Router;
* Axios;
* Pinia, Redux;
* Date processing library;
* UI component library;
* Form validation library.

Install production dependencies:

```bash
npm install axios
```

Or:

```bash
pnpm add axios
```

The package manager will automatically update `package.json`. It is generally not recommended to manually add version numbers.

The criteria for judgment are as follows:

> Will the final application lacking this dependency lose necessary functions?

If so, it should normally be placed at `dependencies`.



#### (5) `devDependencies`: Development dependencies

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

The tools used only during development, compilation, and testing phases are placed here. For example:

* Vite, Webpack;
* TypeScript;
* ESLint;
* Prettier;
* Vitest, Jest;
* Playwright;
* Babel;
* Various compilation plugins;
* Type declaration package.

Install development dependencies:

```bash
npm install eslint --save-dev
```

Abbreviation:

```bash
npm install eslint -D
```

The equivalent of `pnpm`:

```bash
pnpm add eslint -D
```

The official definition of npm is:

* `dependencies`: Required for application production operations;
* `devDependencies`: Required for local development and testing.

For details, see [Explanation of npm dependency categories:](https://docs.npmjs.com/specifying-dependencies-and-devdependencies-in-a-package-json-file/).



A place that can be easily misunderstood.

`vue` and `axios` will eventually be packed into static resources for the pure front end application of the Vite construction and will not be kept in the server `node_modules` as it is.

But they still belong to the functional dependencies of the application. They are usually placed in:

```json
"dependencies"
```

And Vite, ESLint, and TypeScript are build tools. They are placed as follows:

```json
"devDependencies"
```



#### (6) Dependence on version symbols

For example:

```json
{
  "dependencies": {
    "vue": "^3.5.0",
    "axios": "~1.7.2",
    "dayjs": "1.11.13"
  }
}
```



Accurate Version

```json
"dayjs": "1.11.13"
```

Only this version is accepted.

The advantage is that the results are more controllable. The downside is that it does not automatically obtain updates to the revised version.



`^`: Compatible sub-versions and revisions

```json
"vue": "^3.5.0"
```

For normal `1.0.0` and later versions, it is roughly equivalent to:

```text
>=3.5.0 and <4.0.0
```

It can be upgraded:

```text
3.5.1
3.6.0
3.9.9
```

It will not be upgraded to:

```text
4.0.0
```



`~` generally allows patch updates only.

```json
"axios": "~1.7.2"
```

It is roughly equivalent to:

```text
>=1.7.2 and <1.8.0
```

It can be upgraded:

```text
1.7.3
1.7.9
```

It cannot be upgraded to:

```text
1.8.0
```



`*` or `latest`

```json
"some-package": "*"
```

Or use it during installation:

```bash
npm install some-package@latest
```

It is not recommended to use `*` as the dependency in formal projects, as different versions may be obtained during each installation.



The version range does not equal the actual installed version.

Assume that `package.json` contains the following value:

```json
"axios": "^1.7.0"
```

It represents the “allowed version range for installation”, while `package-lock.json`, `pnpm-lock.yaml`, or `yarn.lock` indicate the actual version that is resolved.

Therefore:

* `package.json`: Specify what the project requires.
* Lock file: Record what was specifically installed this time.

Team projects should usually submit a lock file.



#### (7), `type`: Module type

```json
{
  "type": "module"
}
```

It mainly affects how Node.js interprets the `.js` file.



ES Module

```json
{
  "type": "module"
}
```

At this time, the `.js` file uses ESM by default:

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

Or, if `type` is not written, then in a Node.js environment, `.js` will usually be processed according to CommonJS standards:

```js
const fs = require("node:fs");

module.exports = {};
```

Modern Vite front-end projects typically use:

```json
"type": "module"
```

Note that it affects not only the business code, but also:

* `vite.config.js`
* `eslint.config.js`
* Node.js build script
* Test configuration file

In addition:

* `.mjs` Expressed Es Module;
* `.cjs` makes it clear that CommonJs.



#### (8) Node and package manager versions

`engines`

```json
{
  "engines": {
    "node": ">=20.0.0",
    "npm": ">=10.0.0"
  }
}
```

Indicates the operational environment version that the project expects to use.

It is also possible to limit the version range:

```json
{
  "engines": {
    "node": ">=20.19.0 <23"
  }
}
```

It should be noted that `engines` mainly serves as a reminder and constraint in many cases. It does not necessarily prevent the installation by default. Whether the installation will fail strictly depends on the configuration of the package manager.



`packageManager`

```json
{
  "packageManager": "pnpm@9.12.0"
}
```

It indicates which package manager and its version should be used for the project.

Common forms of writing:

```json
"packageManager": "npm@10.8.2"
```

```json
"packageManager": "pnpm@9.12.0"
```

```json
"packageManager": "yarn@4.5.0"
```

It can reduce conflicts in lock files caused by team members using npm, pnpm, and Yarn interchangeably.

It is recommended that a project only uses one type of lock file.

```text
npm   → package-lock.json
pnpm  → pnpm-lock.yaml
Yarn  → yarn.lock
```

Do not submit three lock files at the same time.



## 8. Asynchronous JavaScript

### 8.1, Promise

#### (1) Promise represents future outcomes.

```js
const promise = fetchUser();
```

`promise` is not the final user data, but rather an object that represents future outcomes.

A Promise has three states:

```text
pending    waiting for settlement
fulfilled  completed successfully
rejected   failed
```

The state transition can only occur once:

```text
pending → fulfilled
pending → rejected
```

It cannot be changed again after completion.

#### (2) The Promise executor executes synchronously.

The function that receives `new Promise` is usually called executor.

```js
console.log("A");

const promise = new Promise(resolve => {
  console.log("B");
  resolve("done");
});

console.log("C");
```

Output:

```text
A
B
C
```

The executor executes immediately upon creating the Promise.

The asynchronous part is handled by the Promise handler function that is registered later:

```js
promise.then(value => {
  console.log(value);
});
```

### 8.2, `async` function

#### (1) The `async` function always returns a Promise.

```js
async function getValue() {
  return 42;
}

// The result is a Promise, not a number 42.
const result = getValue();


```

It is approximately equivalent to:

```js
function getValue() {
  return Promise.resolve(42);
}
```

Read the result:

```js
getValue().then(value => {
  console.log(value);
});
```

Or:

```js
const value = await getValue();
```

### 8.3, `await`

#### (1) `await` is waiting for the result of the Promise.

```js
async function loadUser() {
  const user = await fetchUser();
  return user;
}
```

It can be approximated as follows:

```js
function loadUser() {
  return fetchUser().then(user => {
    return user;
  });
}
```

However, `async/await` is usually more readable when it comes to synchronous code.

/*** define element ***/

const body = document.querySelector("body");

//hide screens
const hScreens = document.querySelectorAll(".hScreen"),
   screenExt = document.querySelectorAll(".screen-ext");

//head
const header = document.querySelector("header"),
   navBar = document.querySelector(".nav-bar"),
   menu = document.querySelector(".menu"),
   menuBtn = document.querySelectorAll(".menu-icons"),
   choice = document.querySelector(".choice"),
   choiceBtn = document.querySelectorAll(".choice-open");

//shop page
const filterTitle = document.querySelectorAll(".filter-title"),
   filterBtn = document.querySelectorAll(".filter-open"),
   filterShadow = document.querySelector(".filter-shadow"),
   filterScreen = document.querySelector(".filter-screen"),
   categore = document.querySelectorAll(".categore"),
   catName = document.querySelectorAll(".cat-name"),
   catIn = document.querySelectorAll(".cat-in"),
   cb = document.querySelectorAll("#accept"),
   size = document.querySelectorAll(".size"),
   heart = document.querySelectorAll(".fa-heart");

//product page
const highLight = document.querySelector(".highLight"),
   sImage = document.querySelectorAll(".s-image"),
   colorBox = document.querySelectorAll(".color");

/*** funcutions ***/
const hScreen = {
   open: (el) => {
      el.style.display = "flex";
      body.style.overflow = "hidden";
   },

   cancel: () => {
      body.style.overflow = "visible";
      for (i in hScreens) {
         hScreens[i].style.display = "none";
      }
   },
};

const click = (el, func) => {
   for (let i = 0; i < el.length; i++) {
      el[i].addEventListener("click", func);
   }
};

const navScroll = () => {
   let scroll = window.pageYOffset;
   if (scroll >= header.offsetHeight) {
      navBar.classList.add("nav-bar-f");
   } else {
      navBar.classList.remove("nav-bar-f");
   }
};

/*** events ***/

//nav-bar scrolling
window.addEventListener("scroll", navScroll);

//filter titles click
click(filterTitle, function () {
   for (let i = 0; i < filterTitle.length; i++) {
      filterTitle[i].classList.remove("active-title");
   }
   this.classList.add("active-title");
});

//categore show
for (let i = 0; i < catName.length; i++) {
   catName[i].addEventListener("click", function () {
      catIn[i].classList.toggle("show");
   });
}

//sizes filter clicks
for (let i = 0; i < size.length; i++) {
   size[i].onchange = function () {
      if (cb[i].checked) {
         this.classList.add("active-size");
         this.style.color = "#fff";
      } else {
         this.classList.remove("active-size");
         this.style.color = "#1b262c";
      }
   };
}

//product images change
click(sImage, function () {
   for (let i = 0; i < sImage.length; i++) {
      sImage[i].style.opacity = ".5";
   }
   highLight.src = this.src;
   this.style.opacity = "1";
});

//color select
click(colorBox, function () {
   for (let i = 0; i < colorBox.length; i++) {
      colorBox[i].classList.remove("active-color");
   }

   this.classList.add("active-color");
});

//hide screens clicks
click(menuBtn, hScreen.open.bind(null, menu));
click(choiceBtn, hScreen.open.bind(null, choice));
click(filterBtn, hScreen.open.bind(null, filterShadow));
click(filterBtn, hScreen.open.bind(null, filterScreen));
click(screenExt, hScreen.cancel);

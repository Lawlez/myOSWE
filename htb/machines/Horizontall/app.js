'use strict';
(function(modules) {
  /**
   * @param {!Array} element
   * @return {?}
   */
  function push(element) {
    var moduleId;
    var prop;
    var s = element[0];
    var appliedUpdate = element[1];
    var options = element[2];
    /** @type {number} */
    var i = 0;
    /** @type {!Array} */
    var _sizeAnimateTimeStamps = [];
    for (; i < s.length; i++) {
      prop = s[i];
      if (Object.prototype.hasOwnProperty.call(obj, prop) && obj[prop]) {
        _sizeAnimateTimeStamps.push(obj[prop][0]);
      }
      /** @type {number} */
      obj[prop] = 0;
    }
    for (moduleId in appliedUpdate) {
      if (Object.prototype.hasOwnProperty.call(appliedUpdate, moduleId)) {
        modules[moduleId] = appliedUpdate[moduleId];
      }
    }
    if (addRemoveClassesPostDigest) {
      addRemoveClassesPostDigest(element);
    }
    for (; _sizeAnimateTimeStamps.length;) {
      _sizeAnimateTimeStamps.shift()();
    }
    return result.push.apply(result, options || []), format();
  }
  /**
   * @return {?}
   */
  function format() {
    var ds;
    /** @type {number} */
    var i = 0;
    for (; i < result.length; i++) {
      var data = result[i];
      /** @type {boolean} */
      var a = true;
      /** @type {number} */
      var k = 1;
      for (; k < data.length; k++) {
        var o = data[k];
        if (0 !== obj[o]) {
          /** @type {boolean} */
          a = false;
        }
      }
      if (a) {
        result.splice(i--, 1);
        ds = t(t.s = data[0]);
      }
    }
    return ds;
  }
  /**
   * @param {number} i
   * @return {?}
   */
  function t(i) {
    if (n[i]) {
      return n[i].exports;
    }
    var module = n[i] = {
      i : i,
      l : false,
      exports : {}
    };
    return modules[i].call(module.exports, module, module.exports, t), module.l = true, module.exports;
  }
  var n = {};
  var obj = {
    app : 0
  };
  /** @type {!Array} */
  var result = [];
  t.m = modules;
  t.c = n;
  /**
   * @param {!Function} d
   * @param {string} name
   * @param {!Function} n
   * @return {undefined}
   */
  t.d = function(d, name, n) {
    if (!t.o(d, name)) {
      Object.defineProperty(d, name, {
        enumerable : true,
        get : n
      });
    }
  };
  /**
   * @param {!Object} x
   * @return {undefined}
   */
  t.r = function(x) {
    if ("undefined" !== typeof Symbol && Symbol.toStringTag) {
      Object.defineProperty(x, Symbol.toStringTag, {
        value : "Module"
      });
    }
    Object.defineProperty(x, "__esModule", {
      value : true
    });
  };
  /**
   * @param {number} name
   * @param {number} version
   * @return {?}
   */
  t.t = function(name, version) {
    if (1 & version && (name = t(name)), 8 & version) {
      return name;
    }
    if (4 & version && "object" === typeof name && name && name.__esModule) {
      return name;
    }
    /** @type {!Object} */
    var d = Object.create(null);
    if (t.r(d), Object.defineProperty(d, "default", {
      enumerable : true,
      value : name
    }), 2 & version && "string" != typeof name) {
      var s;
      for (s in name) {
        t.d(d, s, function(nameProp) {
          return name[nameProp];
        }.bind(null, s));
      }
    }
    return d;
  };
  /**
   * @param {!Object} e
   * @return {?}
   */
  t.n = function(e) {
    /** @type {function(): ?} */
    var n = e && e.__esModule ? function() {
      return e["default"];
    } : function() {
      return e;
    };
    return t.d(n, "a", n), n;
  };
  /**
   * @param {!Function} object
   * @param {string} property
   * @return {?}
   */
  t.o = function(object, property) {
    return Object.prototype.hasOwnProperty.call(object, property);
  };
  /** @type {string} */
  t.p = "/";
  var p = window["webpackJsonp"] = window["webpackJsonp"] || [];
  var choiceParagraphElement = p.push.bind(p);
  /** @type {function(!Array): ?} */
  p.push = push;
  p = p.slice();
  /** @type {number} */
  var x = 0;
  for (; x < p.length; x++) {
    push(p[x]);
  }
  var addRemoveClassesPostDigest = choiceParagraphElement;
  result.push([0, "chunk-vendors"]);
  format();
})({
  0 : function(module, checked, e) {
    module.exports = e("56d7");
  },
  "034f" : function(data, linkedEntities, force) {
    force("85ec");
  },
  "1db9" : function(module, abi, name) {
    /** @type {string} */
    module.exports = name.p + "img/c1.2d2dcf21.jpg";
  },
  "215d" : function(mixin, doPost) {
    /** @type {string} */
    mixin.exports = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMIAAAAyCAYAAAAOcwQoAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyZpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMDY3IDc5LjE1Nzc0NywgMjAxNS8wMy8zMC0yMzo0MDo0MiAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTUgKFdpbmRvd3MpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjJDNTQ4NTM3REI5MDExRTlCNDhGQTIwRjNGQTc1N0EzIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjJDNTQ4NTM4REI5MDExRTlCNDhGQTIwRjNGQTc1N0EzIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6MkM1NDg1MzVEQjkwMTFFOUI0OEZBMjBGM0ZBNzU3QTMiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6MkM1NDg1MzZEQjkwMTFFOUI0OEZBMjBGM0ZBNzU3QTMiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz4FAS0XAAAJWElEQVR42uxd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";
  },
  2413 : function(module, abi, name) {
    /** @type {string} */
    module.exports = name.p + "img/coding_.e8413cbf.svg";
  },
  4541 : function(module, abi, name) {
    /** @type {string} */
    module.exports = name.p + "img/handshake.34250d54.svg";
  },
  4851 : function(module, abi, name) {
    /** @type {string} */
    module.exports = name.p + "img/c2.0a3b2b89.jpg";
  },
  "56d7" : function(vdwB, d, $) {
    $.r(d);
    $("e260");
    $("e6cf");
    $("cca6");
    $("a79d");
    var settings = $("2b0e");
    /**
     * @return {?}
     */
    var init = function() {
      var _vm = this;
      var _h = _vm.$createElement;
      var $ = _vm._self._c || _h;
      return $("div", {
        attrs : {
          id : "app"
        }
      }, [$("navbar"), $("home"), _vm._m(0)], 1);
    };
    /** @type {!Array} */
    var artistTrack = [function() {
      var _vm = this;
      var _h = _vm.$createElement;
      var _c = _vm._self._c || _h;
      return _c("footer", {
        staticClass : "gradient"
      }, [_c("div", {
        staticClass : "container-fluid text-center"
      }, [_c("span", [_vm._v("Made by "), _c("a", {
        attrs : {
          href : "https://horizontall.htb"
        }
      }, [_vm._v("Horizontall.htb")])])])]);
    }];
    var s = $("bc3a");
    var r = $.n(s);
    /**
     * @return {?}
     */
    var view = function() {
      var _vm = this;
      var _h = _vm.$createElement;
      var h = _vm._self._c || _h;
      return h("div", [h("b-navbar", {
        attrs : {
          toggleable : "lg",
          type : "light",
          variant : "light"
        }
      }, [h("b-container", [h("b-navbar-brand", {
        attrs : {
          href : "#"
        }
      }, [h("a", {
        attrs : {
          href : "/"
        }
      }, [h("img", {
        attrs : {
          src : $("cc09"),
          alt : ""
        }
      })])]), h("b-navbar-toggle", {
        attrs : {
          target : "nav-collapse"
        }
      }), h("b-collapse", {
        attrs : {
          id : "nav-collapse",
          "is-nav" : ""
        }
      }, [h("b-navbar-nav", {
        staticClass : "ml-auto"
      }, [h("b-nav-item", {
        attrs : {
          href : "#"
        }
      }, [_vm._v("Home")]), h("b-nav-item", {
        attrs : {
          href : "#"
        }
      }, [_vm._v("Feature")]), h("b-nav-item", {
        attrs : {
          href : "#"
        }
      }, [_vm._v("About")])], 1)], 1)], 1)], 1)], 1);
    };
    /** @type {!Array} */
    var item = [];
    var replace = {};
    var parent = replace;
    var attributes = $("2877");
    var module = Object(attributes["a"])(parent, view, item, false, null, null, null);
    var exports_ = module.exports;
    /**
     * @return {?}
     */
    var render = function() {
      var _vm = this;
      var _h = _vm.$createElement;
      var createElement = _vm._self._c || _h;
      return createElement("div", [createElement("header", {
        staticClass : "page-header gradient"
      }, [_vm._m(0), createElement("svg", {
        attrs : {
          xmlns : "http://www.w3.org/2000/svg",
          viewBox : "0 0 1440 250"
        }
      }, [createElement("path", {
        attrs : {
          fill : "#fff",
          "fill-opacity" : "1",
          d : "M0,128L48,117.3C96,107,192,85,288,80C384,75,480,85,576,112C672,139,768,181,864,181.3C960,181,1056,139,1152,122.7C1248,107,1344,117,1392,122.7L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
        }
      })])]), _vm._m(1), createElement("section", {
        staticClass : "feature gradient"
      }, [createElement("svg", {
        attrs : {
          xmlns : "http://www.w3.org/2000/svg",
          viewBox : "0 0 1440 320"
        }
      }, [createElement("path", {
        attrs : {
          fill : "#fff",
          "fill-opacity" : "1",
          d : "M0,224L48,213.3C96,203,192,181,288,154.7C384,128,480,96,576,117.3C672,139,768,213,864,208C960,203,1056,117,1152,101.3C1248,85,1344,139,1392,165.3L1440,192L1440,0L1392,0C1344,0,1248,0,1152,0C1056,0,960,0,864,0C768,0,672,0,576,0C480,0,384,0,288,0C192,0,96,0,48,0L0,0Z"
        }
      })]), _vm._m(2), createElement("svg", {
        attrs : {
          xmlns : "http://www.w3.org/2000/svg",
          viewBox : "0 0 1440 320"
        }
      }, [createElement("path", {
        attrs : {
          fill : "#fff",
          "fill-opacity" : "1",
          d : "M0,224L48,213.3C96,203,192,181,288,154.7C384,128,480,96,576,117.3C672,139,768,213,864,208C960,203,1056,117,1152,101.3C1248,85,1344,139,1392,165.3L1440,192L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
        }
      })])]), createElement("section", {
        staticClass : "icons"
      }, [createElement("div", {
        staticClass : "container"
      }, [createElement("div", {
        staticClass : "row text-center"
      }, [createElement("div", {
        staticClass : "col-md-4"
      }, [createElement("div", {
        staticClass : "icon gradient mb-4"
      }, [createElement("svg", {
        staticClass : "feather feather-layers",
        attrs : {
          xmlns : "http://www.w3.org/2000/svg",
          width : "24",
          height : "24",
          viewBox : "0 0 24 24",
          fill : "none",
          stroke : "currentColor",
          "stroke-width" : "2",
          "stroke-linecap" : "round",
          "stroke-linejoin" : "round"
        }
      }, [createElement("polygon", {
        attrs : {
          points : "12 2 2 7 12 12 22 7 12 2"
        }
      }), createElement("polyline", {
        attrs : {
          points : "2 17 12 22 22 17"
        }
      }), createElement("polyline", {
        attrs : {
          points : "2 12 12 17 22 12"
        }
      })])]), createElement("h3", [_vm._v("Built for developers")]), createElement("p", [_vm._v(" Our customizable, block-based build system makes creating your next project fast and easy! ")])]), createElement("div", {
        staticClass : "col-md-4"
      }, [createElement("div", {
        staticClass : "icon gradient mb-4"
      }, [createElement("svg", {
        staticClass : "feather feather-smartphone",
        attrs : {
          xmlns : "http://www.w3.org/2000/svg",
          width : "24",
          height : "24",
          viewBox : "0 0 24 24",
          fill : "none",
          stroke : "currentColor",
          "stroke-width" : "2",
          "stroke-linecap" : "round",
          "stroke-linejoin" : "round"
        }
      }, [createElement("rect", {
        attrs : {
          x : "5",
          y : "2",
          width : "14",
          height : "20",
          rx : "2",
          ry : "2"
        }
      }), createElement("line", {
        attrs : {
          x1 : "12",
          y1 : "18",
          x2 : "12.01",
          y2 : "18"
        }
      })])]), createElement("h3", [_vm._v("Modern responsive design")]), createElement("p", {
        staticClass : "mb-0"
      }, [_vm._v(" Featuring carefully crafted, mobile-first components, your end product will function beautifully on any device! ")])]), createElement("div", {
        staticClass : "col-md-4"
      }, [createElement("div", {
        staticClass : "icon gradient mb-4"
      }, [createElement("svg", {
        staticClass : "feather feather-code",
        attrs : {
          xmlns : "http://www.w3.org/2000/svg",
          width : "24",
          height : "24",
          viewBox : "0 0 24 24",
          fill : "none",
          stroke : "currentColor",
          "stroke-width" : "2",
          "stroke-linecap" : "round",
          "stroke-linejoin" : "round"
        }
      }, [createElement("polyline", {
        attrs : {
          points : "16 18 22 12 16 6"
        }
      }), createElement("polyline", {
        attrs : {
          points : "8 6 2 12 8 18"
        }
      })])]), createElement("h3", [_vm._v("Complete documentation")]), createElement("p", {
        staticClass : "mb-0"
      }, [_vm._v(" All of the layouts, page sections, components, and utilities are fully covered in this products docs. ")])])])])]), createElement("section", {
        staticClass : "gallery"
      }, [createElement("svg", {
        attrs : {
          xmlns : "http://www.w3.org/2000/svg",
          viewBox : "0 0 1440 160"
        }
      }, [createElement("path", {
        attrs : {
          fill : "#fff",
          "fill-opacity" : "1",
          d : "M0,128L120,128C240,128,480,128,720,122.7C960,117,1200,107,1320,101.3L1440,96L1440,0L1320,0C1200,0,960,0,720,0C480,0,240,0,120,0L0,0Z"
        }
      })]), _vm._m(3), createElement("svg", {
        attrs : {
          xmlns : "http://www.w3.org/2000/svg",
          viewBox : "0 0 1440 320"
        }
      }, [createElement("path", {
        attrs : {
          fill : "#fff",
          "fill-opacity" : "1",
          d : "M0,128L120,128C240,128,480,128,720,122.7C960,117,1200,107,1320,101.3L1440,96L1440,320L1320,320C1200,320,960,320,720,320C480,320,240,320,120,320L0,320Z"
        }
      })])]), createElement("section", {
        staticClass : "services gradient"
      }, [createElement("svg", {
        attrs : {
          xmlns : "http://www.w3.org/2000/svg",
          viewBox : "0 0 1440 220"
        }
      }, [createElement("path", {
        attrs : {
          fill : "#fff",
          "fill-opacity" : "1",
          d : "M0,96L34.3,106.7C68.6,117,137,139,206,122.7C274.3,107,343,53,411,53.3C480,53,549,107,617,117.3C685.7,128,754,96,823,96C891.4,96,960,128,1029,154.7C1097.1,181,1166,203,1234,202.7C1302.9,203,1371,181,1406,170.7L1440,160L1440,0L1405.7,0C1371.4,0,1303,0,1234,0C1165.7,0,1097,0,1029,0C960,0,891,0,823,0C754.3,0,686,0,617,0C548.6,0,480,0,411,0C342.9,0,274,0,206,0C137.1,0,69,0,34,0L0,0Z"
        }
      })]), _vm._m(4), createElement("svg", {
        attrs : {
          xmlns : "http://www.w3.org/2000/svg",
          viewBox : "0 0 1440 210"
        }
      }, [createElement("path", {
        attrs : {
          fill : "#fff",
          "fill-opacity" : "1",
          d : "M0,96L34.3,106.7C68.6,117,137,139,206,122.7C274.3,107,343,53,411,53.3C480,53,549,107,617,117.3C685.7,128,754,96,823,96C891.4,96,960,128,1029,154.7C1097.1,181,1166,203,1234,202.7C1302.9,203,1371,181,1406,170.7L1440,160L1440,320L1405.7,320C1371.4,320,1303,320,1234,320C1165.7,320,1097,320,1029,320C960,320,891,320,823,320C754.3,320,686,320,617,320C548.6,320,480,320,411,320C342.9,320,274,320,206,320C137.1,320,69,320,34,320L0,320Z"
        }
      })])]), _vm._m(5)]);
    };
    /** @type {!Array} */
    var GET_AUTH_URL_TIMEOUT = [function() {
      var _vm = this;
      var _h = _vm.$createElement;
      var _c = _vm._self._c || _h;
      return _c("div", {
        staticClass : "container"
      }, [_c("div", {
        staticClass : "row align-items-center justify-content-center"
      }, [_c("div", {
        staticClass : "col-md-5"
      }, [_c("h2", [_vm._v("Build website using HT")]), _c("p", [_vm._v(" It's crafted with the latest trend of design & coded with all modern approaches. It's a robust & multi-dimensional usable template. ")]), _c("button", {
        staticClass : "btn btn-outline-success btn-lg",
        attrs : {
          type : "button"
        }
      }, [_vm._v(" Read more ")]), _c("button", {
        staticClass : "btn btn-outline-warning btn-lg",
        attrs : {
          type : "button"
        }
      }, [_vm._v(" Play video ")])]), _c("div", {
        staticClass : "col-md-5"
      }, [_c("img", {
        attrs : {
          src : $("e891"),
          alt : "Header image"
        }
      })])])]);
    }, function() {
      var _vm = this;
      var _h = _vm.$createElement;
      var _c = _vm._self._c || _h;
      return _c("section", {
        staticClass : "companies"
      });
    }, function() {
      var _vm = this;
      var _h = _vm.$createElement;
      var _c = _vm._self._c || _h;
      return _c("div", {
        staticClass : "container"
      }, [_c("div", {
        staticClass : "row align-items-center"
      }, [_c("div", {
        staticClass : "col-md-6"
      }, [_c("img", {
        attrs : {
          src : $("fd7d"),
          alt : ""
        }
      })]), _c("div", {
        staticClass : "col-md-6"
      }, [_c("h1", {
        staticClass : "my-3"
      }, [_vm._v("Introducing HT")]), _c("p", {
        staticClass : "my-4"
      }, [_vm._v(" It's crafted with the latest trend of design & coded with all modern approaches. It's a robust & multi-dimensional usable template. ")]), _c("ul", [_c("li", [_vm._v("Best for Creative Agency")]), _c("li", [_vm._v("Built with Latest Technology")]), _c("li", [_vm._v("Super Responsive")]), _c("li", [_vm._v("Creative Design")])])])])]);
    }, function() {
      var _vm = this;
      var _h = _vm.$createElement;
      var _c = _vm._self._c || _h;
      return _c("div", {
        staticClass : "container"
      }, [_c("div", {
        staticClass : "row"
      }, [_c("div", {
        staticClass : "col-md-10"
      }, [_c("h1", [_vm._v("Check our latest awesome creative work")]), _c("p", [_vm._v(" It's crafted with the latest trend of design & coded with all modern approaches. It's a robust & multi-dimensional usable template ")])])]), _c("div", {
        staticClass : "row my-3 g-3"
      }, [_c("div", {
        staticClass : "col-md-4"
      }, [_c("img", {
        staticClass : "img-fluid",
        attrs : {
          src : $("1db9"),
          alt : "Gallery image"
        }
      })]), _c("div", {
        staticClass : "col-md-4"
      }, [_c("img", {
        staticClass : "img-fluid",
        attrs : {
          src : $("4851"),
          alt : "Gallery image"
        }
      })]), _c("div", {
        staticClass : "col-md-4"
      }, [_c("img", {
        staticClass : "img-fluid",
        attrs : {
          src : $("f3ea"),
          alt : "Gallery image"
        }
      })])]), _c("div", {
        staticClass : "row mt-5 justify-content-end"
      }, [_c("div", {
        staticClass : "col-md-2"
      }, [_c("button", {
        staticClass : "btn btn-outline-secondary",
        attrs : {
          type : "button"
        }
      }, [_vm._v(" See all works ")])])])]);
    }, function() {
      var _vm = this;
      var _h = _vm.$createElement;
      var _c = _vm._self._c || _h;
      return _c("div", {
        staticClass : "container"
      }, [_c("div", {
        staticClass : "row align-items-center justify-content-center"
      }, [_c("div", {
        staticClass : "col-md-5"
      }, [_c("button", {
        staticClass : "btn btn-outline-warning mb-3",
        attrs : {
          type : "button"
        }
      }, [_vm._v(" Coding ")]), _c("h1", [_vm._v("We code.")]), _c("p", [_vm._v(" Lorem ipsum dolor sit amet, consectetur adipisicing elit. Delectus, tempore placeat corrupti enim, cumque ex? Mollitia nihil sint cumque omnis iure nisi. ")])]), _c("div", {
        staticClass : "col-md-5"
      }, [_c("img", {
        attrs : {
          src : $("2413"),
          alt : ""
        }
      })]), _c("div", {
        staticClass : "col-md-5"
      }, [_c("img", {
        attrs : {
          src : $("99c0"),
          alt : ""
        }
      })]), _c("div", {
        staticClass : "col-md-5"
      }, [_c("button", {
        staticClass : "btn btn-outline-success mb-3",
        attrs : {
          type : "button "
        }
      }, [_vm._v(" Marketing ")]), _c("h1", [_vm._v("We promote.")]), _c("p", [_vm._v(" Lorem ipsum dolor sit amet, consectetur adipisicing elit. Delectus, tempore placeat corrupti enim, cumque ex? Mollitia nihil sint cumque omnis iure nisi. ")])]), _c("div", {
        staticClass : "col-md-5"
      }, [_c("button", {
        staticClass : "btn btn-outline-light mb-3",
        attrs : {
          type : "button"
        }
      }, [_vm._v(" Selling ")]), _c("h1", [_vm._v("We sell.")]), _c("p", [_vm._v(" Lorem ipsum dolor sit amet, consectetur adipisicing elit. Delectus, tempore placeat corrupti enim, cumque ex? Mollitia nihil sint cumque omnis iure nisi. ")])]), _c("div", {
        staticClass : "col-md-5"
      }, [_c("img", {
        attrs : {
          src : $("6ba1"),
          alt : ""
        }
      })])])]);
    }, function() {
      var _vm = this;
      var _h = _vm.$createElement;
      var h = _vm._self._c || _h;
      return h("section", {
        staticClass : "contact"
      }, [h("div", {
        staticClass : "container"
      }, [h("div", {
        staticClass : "row"
      }, [h("div", {
        staticClass : "col-md-5"
      }, [h("h1", [_vm._v("Contact us:")]), h("div", {
        staticClass : "mb-3"
      }, [h("label", {
        staticClass : "form-label",
        attrs : {
          for : "exampleFormControlInput1"
        }
      }, [_vm._v("Email address")]), h("input", {
        staticClass : "form-control",
        attrs : {
          type : "email",
          id : "exampleFormControlInput1",
          placeholder : "name@example.com"
        }
      })]), h("div", {
        staticClass : "mb-3"
      }, [h("label", {
        staticClass : "form-label",
        attrs : {
          for : "exampleFormControlTextarea1"
        }
      }, [_vm._v("Example textarea")]), h("textarea", {
        staticClass : "form-control",
        attrs : {
          id : "exampleFormControlTextarea1",
          rows : "3"
        }
      })]), h("button", {
        staticClass : "btn btn-outline-secondary",
        attrs : {
          type : "button"
        }
      }, [_vm._v(" Send ")])]), h("div", {
        staticClass : "col-md-5"
      }, [h("img", {
        attrs : {
          src : $("4541"),
          alt : "Contact image"
        }
      })])])])]);
    }];
    var core_user_remove_user_device = {};
    var wsFunction = core_user_remove_user_device;
    var handle = ($("8b71"), Object(attributes["a"])(wsFunction, render, GET_AUTH_URL_TIMEOUT, false, null, null, null));
    var close = handle.exports;
    var config = {
      name : "App",
      components : {
        Navbar : exports_,
        Home : close
      },
      data : function() {
        return {
          reviews : []
        };
      },
      methods : {
        getReviews : function() {
          var $scope = this;
          r.a.get("http://api-prod.horizontall.htb/reviews").then(function(data) {
            return $scope.reviews = data.data;
          });
        }
      }
    };
    var driverDb = config;
    var source = ($("034f"), Object(attributes["a"])(driverDb, init, artistTrack, false, null, null, null));
    var val = source.exports;
    var ext = $("8c4f");
    var args = $("5f5b");
    var filters = $("b1e0");
    $("f9e3");
    $("2dd8");
    settings["default"].use(args["a"]);
    settings["default"].use(filters["a"]);
    settings["default"].use(ext["a"]);
    /** @type {boolean} */
    settings["default"].config.productionTip = false;
    (new settings["default"]({
      render : function(styleHeading) {
        return styleHeading(val);
      }
    })).$mount("#app");
  },
  "6ba1" : function(module, abi, name) {
    /** @type {string} */
    module.exports = name.p + "img/revenue_.71587b74.svg";
  },
  "85ec" : function(enumType, s, wlhash) {
  },
  "88d7" : function(enumType, s, wlhash) {
  },
  "8a45" : function(module, abi, name) {
    /** @type {string} */
    module.exports = name.p + "img/5.5b9914d5.png";
  },
  "8b71" : function(data, linkedEntities, force) {
    force("88d7");
  },
  9689 : function(module, abi, name) {
    /** @type {string} */
    module.exports = name.p + "img/4.52389c77.png";
  },
  "99c0" : function(module, abi, name) {
    /** @type {string} */
    module.exports = name.p + "img/marketing.4b7dfec0.svg";
  },
  ac5a : function(module, abi, name) {
    /** @type {string} */
    module.exports = name.p + "img/1.cecf2cc1.png";
  },
  cc09 : function(module, abi, name) {
    /** @type {string} */
    module.exports = name.p + "img/horizontall.2db2bc37.png";
  },
  e611 : function(module, abi, name) {
    /** @type {string} */
    module.exports = name.p + "img/3.25f11f60.png";
  },
  e891 : function(module, abi, name) {
    /** @type {string} */
    module.exports = name.p + "img/email_campaign_monochromatic.f0faa6a4.svg";
  },
  eafb : function(module, abi, name) {
    /** @type {string} */
    module.exports = name.p + "img/2.76afc074.png";
  },
  f3ea : function(module, abi, name) {
    /** @type {string} */
    module.exports = name.p + "img/c3.1a5adf9b.jpg";
  },
  fd7d : function(module, abi, name) {
    /** @type {string} */
    module.exports = name.p + "img/seo_monochromatic.5fce4827.svg";
  }
});

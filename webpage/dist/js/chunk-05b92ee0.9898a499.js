(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-05b92ee0"],{"00d87":function(t,e){(function(){var e="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",a={rotl:function(t,e){return t<<e|t>>>32-e},rotr:function(t,e){return t<<32-e|t>>>e},endian:function(t){if(t.constructor==Number)return 16711935&a.rotl(t,8)|4278255360&a.rotl(t,24);for(var e=0;e<t.length;e++)t[e]=a.endian(t[e]);return t},randomBytes:function(t){for(var e=[];t>0;t--)e.push(Math.floor(256*Math.random()));return e},bytesToWords:function(t){for(var e=[],a=0,n=0;a<t.length;a++,n+=8)e[n>>>5]|=t[a]<<24-n%32;return e},wordsToBytes:function(t){for(var e=[],a=0;a<32*t.length;a+=8)e.push(t[a>>>5]>>>24-a%32&255);return e},bytesToHex:function(t){for(var e=[],a=0;a<t.length;a++)e.push((t[a]>>>4).toString(16)),e.push((15&t[a]).toString(16));return e.join("")},hexToBytes:function(t){for(var e=[],a=0;a<t.length;a+=2)e.push(parseInt(t.substr(a,2),16));return e},bytesToBase64:function(t){for(var a=[],n=0;n<t.length;n+=3)for(var s=t[n]<<16|t[n+1]<<8|t[n+2],i=0;i<4;i++)8*n+6*i<=8*t.length?a.push(e.charAt(s>>>6*(3-i)&63)):a.push("=");return a.join("")},base64ToBytes:function(t){t=t.replace(/[^A-Z0-9+\/]/gi,"");for(var a=[],n=0,s=0;n<t.length;s=++n%4)0!=s&&a.push((e.indexOf(t.charAt(n-1))&Math.pow(2,-2*s+8)-1)<<2*s|e.indexOf(t.charAt(n))>>>6-2*s);return a}};t.exports=a})()},"1e7e":function(t,e,a){"use strict";a.r(e);var n=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("Row",{attrs:{gutter:10}},[a("Col",{attrs:{span:"14"}},[a("Card",{staticStyle:{"margin-bottom":"10px"}},[a("p",{attrs:{slot:"title"},slot:"title"},[t._v("基本信息")]),a("Form",{attrs:{"label-width":90}},[a("FormItem",{staticStyle:{"margin-bottom":"5px"},attrs:{label:"主机名:"}},[a("span",{staticClass:"instance-content"},[t._v(t._s(t.instanceData.hostname))])]),a("FormItem",{directives:[{name:"show",rawName:"v-show",value:"native"===t.cmdb,expression:"cmdb === 'native'"}],staticStyle:{"margin-bottom":"5px"},attrs:{label:"IDC:"}},[a("span",{staticClass:"instance-content"},[t._v(t._s(t.instanceData.idc))])]),a("FormItem",{directives:[{name:"show",rawName:"v-show",value:"native"===t.cmdb,expression:"cmdb === 'native'"}],staticStyle:{"margin-bottom":"5px"},attrs:{label:"描述:"}},[a("span",{staticClass:"instance-content"},[t._v(t._s(t.instanceData.description))])]),a("FormItem",{directives:[{name:"show",rawName:"v-show",value:"aliyun"===t.cmdb,expression:"cmdb === 'aliyun'"}],staticStyle:{"margin-bottom":"5px"},attrs:{label:"可用区:"}},[a("span",{staticClass:"instance-content"},[t._v(t._s(t.instanceData.zone_id))])]),a("FormItem",{directives:[{name:"show",rawName:"v-show",value:"aliyun"===t.cmdb,expression:"cmdb === 'aliyun'"}],staticStyle:{"margin-bottom":"5px"},attrs:{label:"名称:"}},[a("span",{staticClass:"instance-content"},[t._v(t._s(t.instanceData.instance_name))])]),a("FormItem",{directives:[{name:"show",rawName:"v-show",value:"aliyun"===t.cmdb,expression:"cmdb === 'aliyun'"}],staticStyle:{"margin-bottom":"5px"},attrs:{label:"ID:"}},[a("span",{staticClass:"instance-content"},[t._v(t._s(t.instanceData.instance_id))])]),a("FormItem",{directives:[{name:"show",rawName:"v-show",value:"aliyun"===t.cmdb,expression:"cmdb === 'aliyun'"}],staticStyle:{"margin-bottom":"5px"},attrs:{label:"实例规格:"}},[a("span",{staticClass:"instance-content"},[t._v(t._s(t.instanceData.instance_type))])]),a("FormItem",{directives:[{name:"show",rawName:"v-show",value:"aliyun"===t.cmdb,expression:"cmdb === 'aliyun'"}],staticStyle:{"margin-bottom":"5px"},attrs:{label:"付费方式:"}},[a("span",{staticClass:"instance-content"},[t._v(t._s(t.instanceData.instance_charge_type))])]),a("FormItem",{directives:[{name:"show",rawName:"v-show",value:"aliyun"===t.cmdb,expression:"cmdb === 'aliyun'"}],staticStyle:{"margin-bottom":"5px"},attrs:{label:"创建时间:"}},[a("span",{staticClass:"instance-content"},[t._v(t._s(t.instanceData.created))])]),a("FormItem",{directives:[{name:"show",rawName:"v-show",value:"aliyun"===t.cmdb,expression:"cmdb === 'aliyun'"}],staticStyle:{"margin-bottom":"5px"},attrs:{label:"最后更新时间:"}},[a("span",{staticClass:"instance-content"},[t._v(t._s(t.instanceData.updated))])]),a("FormItem",{directives:[{name:"show",rawName:"v-show",value:"aliyun"===t.cmdb,expression:"cmdb === 'aliyun'"}],staticStyle:{"margin-bottom":"5px"},attrs:{label:"过期时间:"}},[a("span",{staticClass:"instance-content"},[t._v(t._s(t.instanceData.expired_time))])]),a("FormItem",{staticStyle:{"margin-bottom":"5px"},attrs:{label:"SN:"}},[a("span",{staticClass:"instance-content"},[t._v(t._s(t.instanceData.serial_number))])])],1)],1),a("Card",[a("p",{attrs:{slot:"title"},slot:"title"},[t._v("配置信息")]),a("Form",{attrs:{"label-width":80}},[a("FormItem",{staticStyle:{"margin-bottom":"5px"},attrs:{label:"环境:"}},[a("span",{staticClass:"instance-content"},[t._v(t._s(t.instanceData.environment))])]),a("FormItem",{staticStyle:{"margin-bottom":"5px"},attrs:{label:"CPU:"}},[a("span",{staticClass:"instance-content"},[t._v(t._s(t.instanceData.cpu))])]),a("FormItem",{staticStyle:{"margin-bottom":"5px"},attrs:{label:"内存:"}},[a("span",{staticClass:"instance-content"},[t._v(t._s(t.instanceData.memory)+" MB")])]),a("FormItem",{staticStyle:{"margin-bottom":"5px"},attrs:{label:"磁盘:"}},[a("span",{staticClass:"instance-content"},[t._v(t._s(t.instanceData.disk))])]),a("FormItem",{staticStyle:{"margin-bottom":"5px"},attrs:{label:"操作系统:"}},[a("span",{staticClass:"instance-content"},[t._v(t._s(t.instanceData.os_name))])]),a("FormItem",{staticStyle:{"margin-bottom":"5px"},attrs:{label:"公网IP:"}},[a("span",{staticClass:"instance-content"},[t._v(t._s(t.instanceData.public_ip))])]),a("FormItem",{staticStyle:{"margin-bottom":"5px"},attrs:{label:"私网IP:"}},[a("span",{staticClass:"instance-content"},[t._v(t._s(t.instanceData.private_ip))])]),a("FormItem",{staticStyle:{"margin-bottom":"5px"},attrs:{label:"SSH IP:"}},[a("span",{staticClass:"instance-content"},[t._v(t._s(t.instanceData.ssh_ip))])]),a("FormItem",{staticStyle:{"margin-bottom":"5px"},attrs:{label:"SSH Port:"}},[a("span",{staticClass:"instance-content"},[t._v(t._s(t.instanceData.ssh_port))])])],1)],1)],1),a("Col",{attrs:{span:"10"}},[a("Card",{staticStyle:{"margin-bottom":"10px"}},[a("p",{attrs:{slot:"title"},slot:"title"},[t._v("状态")]),a("Row",{attrs:{gutter:10}},[a("Col",{attrs:{span:"4"}},[a("p",{staticStyle:{"text-align":"center"}},[a("Icon",{directives:[{name:"show",rawName:"v-show",value:"Running"===t.instanceData.status,expression:"instanceData.status === 'Running'"}],staticStyle:{"font-size":"40px",color:"#67C23A"},attrs:{type:"md-arrow-dropright-circle"}}),a("Icon",{directives:[{name:"show",rawName:"v-show",value:"Running"!==t.instanceData.status,expression:"instanceData.status !== 'Running'"}],staticStyle:{"font-size":"40px",color:"#F56C6C"},attrs:{type:"md-pause"}}),a("br"),a("span",{directives:[{name:"show",rawName:"v-show",value:"Running"===t.instanceData.status,expression:"instanceData.status === 'Running'"}],staticStyle:{color:"#67C23A"}},[t._v("运行中")]),a("span",{directives:[{name:"show",rawName:"v-show",value:"Running"!==t.instanceData.status,expression:"instanceData.status !== 'Running'"}],staticStyle:{color:"#F56C6C"}},[t._v("停止")])],1)]),a("Col",{attrs:{span:"4"}},[a("p",{staticStyle:{"text-align":"center"}},[a("Icon",{directives:[{name:"show",rawName:"v-show",value:t.instanceData.is_active,expression:"instanceData.is_active"}],staticStyle:{"font-size":"40px",color:"#67C23A"},attrs:{type:"md-checkmark-circle-outline"}}),a("Icon",{directives:[{name:"show",rawName:"v-show",value:!t.instanceData.is_active,expression:"!instanceData.is_active"}],staticStyle:{"font-size":"40px",color:"#F56C6C"},attrs:{type:"ios-remove-circle-outline"}}),a("br"),a("span",{directives:[{name:"show",rawName:"v-show",value:t.instanceData.is_active,expression:"instanceData.is_active"}],staticStyle:{color:"#67C23A"}},[t._v("使用中")]),a("span",{directives:[{name:"show",rawName:"v-show",value:!t.instanceData.is_active,expression:"!instanceData.is_active"}],staticStyle:{color:"#F56C6C"}},[t._v("回收")])],1)]),a("Col",{attrs:{span:"4"}},[a("p",{staticStyle:{"text-align":"center"}},[a("Icon",{directives:[{name:"show",rawName:"v-show",value:t.instanceData.is_ansible,expression:"instanceData.is_ansible"}],staticStyle:{"font-size":"40px",color:"#67C23A"},attrs:{type:"md-checkmark-circle-outline"}}),a("Icon",{directives:[{name:"show",rawName:"v-show",value:!t.instanceData.is_ansible,expression:"!instanceData.is_ansible"}],staticStyle:{"font-size":"40px",color:"#F56C6C"},attrs:{type:"ios-close-circle-outline"}}),a("br"),a("span",{directives:[{name:"show",rawName:"v-show",value:t.instanceData.is_ansible,expression:"instanceData.is_ansible"}],staticStyle:{color:"#67C23A"}},[t._v("激活 Ansible")]),a("span",{directives:[{name:"show",rawName:"v-show",value:!t.instanceData.is_ansible,expression:"!instanceData.is_ansible"}],staticStyle:{color:"#F56C6C"}},[t._v("禁用 Ansible")])],1)])],1)],1),a("Card",{staticStyle:{"margin-bottom":"10px"}},[a("p",{attrs:{slot:"title"},slot:"title"},[t._v("操作")]),a("Form",{attrs:{"label-width":100}},[a("FormItem",{attrs:{label:"Ansible 更新:"}},[a("Button",{staticStyle:{float:"right"},attrs:{type:"primary",ghost:"",loading:t.ansibleLoading,disabled:!t.instanceData.is_ansible},on:{click:t.ansibleUpdate}},[t._v("执行")])],1)],1)],1),a("Card",[a("p",{attrs:{slot:"title"},slot:"title"},[t._v("App")]),a("Table",{attrs:{columns:t.tableColumns,data:t.tableDatas}})],1)],1)],1)],1)},s=[],i=a("ce91"),r=a("a260"),o=a("c276"),c={name:"cmdb_host_info",watch:{id:function(t,e){var a=this;void 0!==t&&this.$route.query.cmdb&&(this.reloadInfo(this.cmdb),setTimeout(function(){a.$Spin.hide()},800),this.$Spin.show({render:function(t){return t("div",[t("Icon",{class:"demo-spin-icon-load",props:{type:"ios-loading",size:18}}),t("div","Loading")])}}))}},computed:{id:{get:function(){return this.$route.params.id},set:function(t){return t}},cmdb:{get:function(){return this.$route.query.cmdb},set:function(t){return t}}},data:function(){var t=this,e=function(t,e){return t("Icon",e?{props:{type:"md-checkmark-circle-outline"},style:{color:"#67C23A","font-size":"20px"}}:{props:{type:"ios-close-circle-outline"},style:{color:"#ed4014","font-size":"20px"}})};return{ansibleLoading:!1,tableColumns:[{title:"Name",key:"app_name",render:function(e,a){return e("a",{on:{click:function(){var e=a.row.id,n=a.row.app_name,s={name:"apps_app_detail",params:{id:e},query:{app_name:n}};t.$router.push(s)}}},a.row.app_name)}},{title:"Used",key:"is_active",align:"center",render:function(t,a){var n=a.row.is_active;return e(t,n)}}],tableDatas:[],instanceData:{}}},methods:{ansibleUpdate:function(){var t=this;this.ansibleLoading=!0;var e={cmdb:this.cmdb,single_host_id:this.id};try{switch(this.cmdb){case"aliyun":Object(i["b"])(e).then(function(e){t.$Message.success("操作成功"),t.reloadInfo(t.cmdb),t.ansibleLoading=!1}).catch(function(e){Object(o["s"])("error",e),t.ansibleLoading=!1});break;case"native":Object(r["d"])(e).then(function(e){t.$Message.success("操作成功"),t.reloadInfo(t.cmdb),t.ansibleLoading=!1}).catch(function(e){Object(o["s"])("error",e),t.ansibleLoading=!1});break}}catch(a){Object(o["s"])("error",a),this.ansibleLoading=!1}},reloadInfo:function(t){var e=this,a={aliyun:i["n"],native:r["m"]},n={aliyun:i["f"],native:r["i"]};a[t](this.id).then(function(t){e.instanceData=t.data,e.instanceData.private_ip=JSON.parse(e.instanceData.private_ip).join("; "),e.instanceData.public_ip=JSON.parse(e.instanceData.public_ip).join("; ");var a=[],n=JSON.parse(e.instanceData.disk);for(var s in n)a.push("".concat(s,": ").concat(n[s]," GiB"));e.instanceData.disk=a.join("; ")}).catch(function(t){Object(o["s"])("error",t)}),n[t](this.id).then(function(t){e.tableDatas=t.data}).catch(function(t){Object(o["s"])("error",t)})}},mounted:function(){this.cmdb=this.$route.query.cmdb,this.id=this.$route.params.id,this.reloadInfo(this.cmdb)}},u=c,l=(a("a95c"),a("2877")),d=Object(l["a"])(u,n,s,!1,null,null,null);d.options.__file="single_instance.vue";e["default"]=d.exports},"55e1":function(t,e,a){},"6821f":function(t,e,a){(function(){var e=a("00d87"),n=a("9a63").utf8,s=a("044b"),i=a("9a63").bin,r=function(t,a){t.constructor==String?t=a&&"binary"===a.encoding?i.stringToBytes(t):n.stringToBytes(t):s(t)?t=Array.prototype.slice.call(t,0):Array.isArray(t)||(t=t.toString());for(var o=e.bytesToWords(t),c=8*t.length,u=1732584193,l=-271733879,d=-1732584194,m=271733878,p=0;p<o.length;p++)o[p]=16711935&(o[p]<<8|o[p]>>>24)|4278255360&(o[p]<<24|o[p]>>>8);o[c>>>5]|=128<<c%32,o[14+(c+64>>>9<<4)]=c;var h=r._ff,v=r._gg,b=r._hh,f=r._ii;for(p=0;p<o.length;p+=16){var y=u,g=l,_=d,w=m;u=h(u,l,d,m,o[p+0],7,-680876936),m=h(m,u,l,d,o[p+1],12,-389564586),d=h(d,m,u,l,o[p+2],17,606105819),l=h(l,d,m,u,o[p+3],22,-1044525330),u=h(u,l,d,m,o[p+4],7,-176418897),m=h(m,u,l,d,o[p+5],12,1200080426),d=h(d,m,u,l,o[p+6],17,-1473231341),l=h(l,d,m,u,o[p+7],22,-45705983),u=h(u,l,d,m,o[p+8],7,1770035416),m=h(m,u,l,d,o[p+9],12,-1958414417),d=h(d,m,u,l,o[p+10],17,-42063),l=h(l,d,m,u,o[p+11],22,-1990404162),u=h(u,l,d,m,o[p+12],7,1804603682),m=h(m,u,l,d,o[p+13],12,-40341101),d=h(d,m,u,l,o[p+14],17,-1502002290),l=h(l,d,m,u,o[p+15],22,1236535329),u=v(u,l,d,m,o[p+1],5,-165796510),m=v(m,u,l,d,o[p+6],9,-1069501632),d=v(d,m,u,l,o[p+11],14,643717713),l=v(l,d,m,u,o[p+0],20,-373897302),u=v(u,l,d,m,o[p+5],5,-701558691),m=v(m,u,l,d,o[p+10],9,38016083),d=v(d,m,u,l,o[p+15],14,-660478335),l=v(l,d,m,u,o[p+4],20,-405537848),u=v(u,l,d,m,o[p+9],5,568446438),m=v(m,u,l,d,o[p+14],9,-1019803690),d=v(d,m,u,l,o[p+3],14,-187363961),l=v(l,d,m,u,o[p+8],20,1163531501),u=v(u,l,d,m,o[p+13],5,-1444681467),m=v(m,u,l,d,o[p+2],9,-51403784),d=v(d,m,u,l,o[p+7],14,1735328473),l=v(l,d,m,u,o[p+12],20,-1926607734),u=b(u,l,d,m,o[p+5],4,-378558),m=b(m,u,l,d,o[p+8],11,-2022574463),d=b(d,m,u,l,o[p+11],16,1839030562),l=b(l,d,m,u,o[p+14],23,-35309556),u=b(u,l,d,m,o[p+1],4,-1530992060),m=b(m,u,l,d,o[p+4],11,1272893353),d=b(d,m,u,l,o[p+7],16,-155497632),l=b(l,d,m,u,o[p+10],23,-1094730640),u=b(u,l,d,m,o[p+13],4,681279174),m=b(m,u,l,d,o[p+0],11,-358537222),d=b(d,m,u,l,o[p+3],16,-722521979),l=b(l,d,m,u,o[p+6],23,76029189),u=b(u,l,d,m,o[p+9],4,-640364487),m=b(m,u,l,d,o[p+12],11,-421815835),d=b(d,m,u,l,o[p+15],16,530742520),l=b(l,d,m,u,o[p+2],23,-995338651),u=f(u,l,d,m,o[p+0],6,-198630844),m=f(m,u,l,d,o[p+7],10,1126891415),d=f(d,m,u,l,o[p+14],15,-1416354905),l=f(l,d,m,u,o[p+5],21,-57434055),u=f(u,l,d,m,o[p+12],6,1700485571),m=f(m,u,l,d,o[p+3],10,-1894986606),d=f(d,m,u,l,o[p+10],15,-1051523),l=f(l,d,m,u,o[p+1],21,-2054922799),u=f(u,l,d,m,o[p+8],6,1873313359),m=f(m,u,l,d,o[p+15],10,-30611744),d=f(d,m,u,l,o[p+6],15,-1560198380),l=f(l,d,m,u,o[p+13],21,1309151649),u=f(u,l,d,m,o[p+4],6,-145523070),m=f(m,u,l,d,o[p+11],10,-1120210379),d=f(d,m,u,l,o[p+2],15,718787259),l=f(l,d,m,u,o[p+9],21,-343485551),u=u+y>>>0,l=l+g>>>0,d=d+_>>>0,m=m+w>>>0}return e.endian([u,l,d,m])};r._ff=function(t,e,a,n,s,i,r){var o=t+(e&a|~e&n)+(s>>>0)+r;return(o<<i|o>>>32-i)+e},r._gg=function(t,e,a,n,s,i,r){var o=t+(e&n|a&~n)+(s>>>0)+r;return(o<<i|o>>>32-i)+e},r._hh=function(t,e,a,n,s,i,r){var o=t+(e^a^n)+(s>>>0)+r;return(o<<i|o>>>32-i)+e},r._ii=function(t,e,a,n,s,i,r){var o=t+(a^(e|~n))+(s>>>0)+r;return(o<<i|o>>>32-i)+e},r._blocksize=16,r._digestsize=16,t.exports=function(t,a){if(void 0===t||null===t)throw new Error("Illegal argument "+t);var n=e.wordsToBytes(r(t,a));return a&&a.asBytes?n:a&&a.asString?i.bytesToString(n):e.bytesToHex(n)}})()},"9a63":function(t,e){var a={utf8:{stringToBytes:function(t){return a.bin.stringToBytes(unescape(encodeURIComponent(t)))},bytesToString:function(t){return decodeURIComponent(escape(a.bin.bytesToString(t)))}},bin:{stringToBytes:function(t){for(var e=[],a=0;a<t.length;a++)e.push(255&t.charCodeAt(a));return e},bytesToString:function(t){for(var e=[],a=0;a<t.length;a++)e.push(String.fromCharCode(t[a]));return e.join("")}}};t.exports=a},a260:function(t,e,a){"use strict";a.d(e,"g",function(){return r}),a.d(e,"j",function(){return o}),a.d(e,"h",function(){return c}),a.d(e,"b",function(){return u}),a.d(e,"k",function(){return l}),a.d(e,"f",function(){return d}),a.d(e,"l",function(){return m}),a.d(e,"a",function(){return p}),a.d(e,"n",function(){return h}),a.d(e,"m",function(){return v}),a.d(e,"e",function(){return b}),a.d(e,"d",function(){return f}),a.d(e,"c",function(){return y}),a.d(e,"i",function(){return g});var n=a("66df"),s=a("6821f"),i={pp:s("cmdb_native_resource")},r=function(){return n["a"].request({url:"/api/v1/common/setting/cmdb/",method:"get",headers:i})},o=function(){return n["a"].request({url:"/api/v1/cmdb/native/host/",method:"get",headers:i})},c=function(t){return n["a"].request({url:"/api/v1/cmdb/native/classify/?search=".concat(t),method:"get",headers:i})},u=function(t){return n["a"].request({url:"/api/v1/cmdb/tags-rel/native-host/",method:"post",data:t,headers:i})},l=function(t){return n["a"].request({url:"/api/v1/cmdb/tags-rel/native-host/?target_id=".concat(t),method:"get",headers:i})},d=function(t){return n["a"].request({url:"/api/v1/cmdb/tags-rel/native-host/".concat(t,"/"),method:"delete",headers:i})},m=function(){return n["a"].request({url:"/api/v1/cmdb/tags/",method:"get",headers:i})},p=function(t){return n["a"].request({url:"/api/v1/cmdb/native/host/",method:"post",data:t,headers:i})},h=function(t,e){return n["a"].request({url:"/api/v1/cmdb/native/host/".concat(t,"/"),method:"put",data:e,headers:i})},v=function(t){return n["a"].request({url:"/api/v1/cmdb/native/host/".concat(t,"/"),method:"get",headers:i})},b=function(t){return n["a"].request({url:"/api/v1/cmdb/native/host/".concat(t,"/"),method:"delete",headers:i})},f=function(t){return n["a"].request({url:"/api/v1/cmdb/ansible/update/",method:"post",data:t,headers:i})},y=function(t){return n["a"].request({url:"/api/v1/cmdb/ansible/add/",method:"post",data:t,headers:i})},g=function(t){return n["a"].request({url:"/api/v1/cmdb/native/rel/host-app/".concat(t,"/"),method:"get",headers:i})}},a95c:function(t,e,a){"use strict";var n=a("55e1"),s=a.n(n);s.a},ce91:function(t,e,a){"use strict";a.d(e,"j",function(){return r}),a.d(e,"e",function(){return o}),a.d(e,"h",function(){return c}),a.d(e,"k",function(){return u}),a.d(e,"o",function(){return l}),a.d(e,"p",function(){return d}),a.d(e,"d",function(){return m}),a.d(e,"n",function(){return p}),a.d(e,"g",function(){return h}),a.d(e,"m",function(){return v}),a.d(e,"c",function(){return b}),a.d(e,"a",function(){return f}),a.d(e,"b",function(){return y}),a.d(e,"f",function(){return g}),a.d(e,"i",function(){return _}),a.d(e,"l",function(){return w}),a.d(e,"q",function(){return x});var n=a("66df"),s=a("6821f"),i={pp:s("cmdb_aliyun_resource")},r=function(){return n["a"].request({url:"/api/v1/common/setting/cmdb/",method:"get",headers:i})},o=function(){return n["a"].request({url:"/api/v1/cmdb/aliyun/keys/",method:"get",headers:i})},c=function(t){return n["a"].request({url:"/api/v1/cmdb/aliyun/classify/?search=".concat(t),method:"get",headers:i})},u=function(){return n["a"].request({url:"/api/v1/cmdb/aliyun/ecs/",method:"get",headers:i})},l=function(t){return n["a"].request({url:"/api/v1/cmdb/aliyun/ecs-auto/",method:"post",data:t,headers:i})},d=function(t,e){return n["a"].request({url:"/api/v1/cmdb/aliyun/ecs/".concat(t,"/"),method:"put",data:e,headers:i})},m=function(t){return n["a"].request({url:"/api/v1/cmdb/aliyun/ecs/".concat(t,"/"),method:"delete",headers:i})},p=function(t){return n["a"].request({url:"/api/v1/cmdb/aliyun/ecs/".concat(t,"/"),method:"get",headers:i})},h=function(t){return n["a"].request({url:"/api/v1/cmdb/tags-rel/aliyun-ecs/?target_id=".concat(t),method:"get",headers:i})},v=function(){return n["a"].request({url:"/api/v1/cmdb/tags/",method:"get",headers:i})},b=function(t){return n["a"].request({url:"/api/v1/cmdb/tags-rel/aliyun-ecs/".concat(t,"/"),method:"delete",headers:i})},f=function(t){return n["a"].request({url:"/api/v1/cmdb/tags-rel/aliyun-ecs/",method:"post",data:t,headers:i})},y=function(t){return n["a"].request({url:"/api/v1/cmdb/ansible/update/",method:"post",data:t,headers:i})},g=function(t){return n["a"].request({url:"/api/v1/cmdb/aliyun/rel/ecs-app/".concat(t,"/"),method:"get",headers:i})},_=function(t){return n["a"].request({url:"/api/v1/cmdb/aliyun/rds/classify/?search=".concat(t),method:"get",headers:i})},w=function(){return n["a"].request({url:"/api/v1/cmdb/aliyun/rds/classify/",method:"get",headers:i})},x=function(t,e){return n["a"].request({url:"/api/v1/cmdb/aliyun/rds/classify/".concat(t,"/"),method:"put",headers:i,data:e})}}}]);
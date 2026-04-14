/* esm.sh - framer-motion@10.16.4/dist/es/utils/delay */
import{frame as s,cancelFrame as c}from"./framer-motion_at_10.16.4_X-ZHJlYWN0LWRvbUAxOC4yLjAscmVhY3RAMTguMi4w_es2022_dist_es_utils_.._frameloop_frame.mjs";function p(n,r){let o=performance.now(),e=({timestamp:t})=>{let a=t-o;a>=r&&(c(e),n(a-r))};return s.read(e,!0),()=>c(e)}export{p as delay};
//# sourceMappingURL=delay.mjs.map
// import random, { Random } from "random";

// import { beta } from "@stdlib/stats-base-dists/docs/types";


// class Distribution {
    
//     *generate_value() {
//         console.log("generate value abstract method");
//         yield;
//     }

//     get_info() {
//         console.log('get info abstract method');
//     }

//   }

// class Normal extends Distribution {


//     static dist_type = 'Normal';

//     constructor(mean, sd){
//         this.mean=mean
//         this.sd=sd
//         this.generator = random.normal(mead, sd)

//     }

//     /**
//      * Returns random value from set normal dist
//      * @return {number}
//     */
//     *generate_value(){
//         yield this.generator()
//     }

//     get_info(){
//         return {
//             "dist_type":'Normal',
//             'mean': this.mean,
//             'sd': this.sd,
//             'str_format': `NormalDist(${this.mean}, ${this.sd})`
//         } 
//     }
// }

// class BetaDist extends Distribution {
    
//     static dist_type = 'Beta';

//     constructor(a, b, scale){
//         this.a = a
//         this.b = b
//         this.scale = this.scale
//         this.generator = random.normal(a, b)
//     }


//     get_info(){
//         return {
//             "dist_type":'Normal',
//             'a': this.a,
//             'b': this.b,
//             'str_format': `BetaDist(${this.a}, ${this.b} , ${this.scale})`
//         } 
//     }
// }
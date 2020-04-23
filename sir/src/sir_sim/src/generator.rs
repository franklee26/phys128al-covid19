/*
* generator.rs
* Frank Lee 23/4
* Module for generator S I R data (Python is slow...)
*/
use rand::distributions::WeightedIndex;
use rand::prelude::*;
use std::fs;

/*
 * Initial vars temporarily set here for now
 * S_0 = N = 10000
 * I_0 = 1
 * R_0 = 0
 */
const K: f64 = 0.5;
const S_0: f64 = 10000.0;
const N: f64 = 10000.0;
const I_0: f64 = 1.0;
const R_0: f64 = 0.0;
const GAMMA: f64 = 0.2;

pub struct Generator {
    pub s_set: Vec<Vec<f64>>,
    pub i_set: Vec<Vec<f64>>,
    pub r_set: Vec<Vec<f64>>,
    num_trials: usize,
    num_steps: usize,
    time_step: f64,
}

impl Generator {
    pub fn new(num_trials: usize, num_steps: usize, time_step: f64) -> Generator {
        Generator {
            num_trials: num_trials,
            num_steps: num_steps,
            time_step: time_step,
            s_set: vec![vec![0.0; num_steps]; num_trials],
            i_set: vec![vec![0.0; num_steps]; num_trials],
            r_set: vec![vec![0.0; num_steps]; num_trials],
        }
    }

    /*
     * private generator that computes a single SIR trial
     * and will be used for multiple trials
     */
    fn sir(&self) -> Vec<Vec<f64>> {
        // S = [0], I = [1], R = [2]
        let mut one_sir = vec![vec![S_0], vec![I_0], vec![R_0]];
        for _ in 0..self.num_steps {
            let &s_last = one_sir[0].last().unwrap();
            let &i_last = one_sir[1].last().unwrap();
            let &r_last = one_sir[2].last().unwrap();
            let infection: f64 = K * s_last * i_last * self.time_step / N;
            let recovery: f64 = GAMMA * i_last * self.time_step;
            let mut nothing: f64 = 1.0 - infection - recovery;
            if nothing < 0.0 {
                nothing = 0.0;
            }

            // build a random weighted chooser
            let weights = [nothing, infection, recovery];
            let choice = [0, 1, 2];
            let dist = WeightedIndex::new(&weights).unwrap();
            let mut rng = thread_rng();

            match choice[dist.sample(&mut rng)] {
                0 => {
                    // do nothing
                    one_sir[0].push(s_last);
                    one_sir[1].push(i_last);
                    one_sir[2].push(r_last);
                }
                1 => {
                    // infection
                    one_sir[0].push(s_last - 1.0);
                    one_sir[1].push(i_last + 1.0);
                    one_sir[2].push(r_last);
                }
                2 => {
                    // recovery
                    one_sir[0].push(s_last);
                    one_sir[1].push(i_last - 1.0);
                    one_sir[2].push(r_last + 1.0);
                }
                _ => {
                    // do nothing
                    one_sir[0].push(s_last);
                    one_sir[1].push(i_last);
                    one_sir[2].push(r_last);
                }
            }
        }
        return one_sir;
    }

    /*
     * public function setter that will build the trial
     * sets
     */
    pub fn sir_trials(&mut self) {
        for i in 0..self.num_trials {
            let mut one_trial = self.sir();

            // weird error checking...
            while (one_trial[0][0] - one_trial[0].last().unwrap()).abs() < 10.0 {
                one_trial = self.sir();
            }
            self.s_set[i] = one_trial[0].clone();
            self.i_set[i] = one_trial[1].clone();
            self.r_set[i] = one_trial[2].clone();
        }
    }

    pub fn write_data(&mut self) {
        let mut s_data_str: Vec<String> = vec![];
        for i in 0..self.s_set.len() {
            s_data_str.push(
                self.s_set[i]
                    .clone()
                    .into_iter()
                    .map(|i| i.to_string() + "\n")
                    .collect::<String>(),
            );
        }
        fs::write("../data/s_data.txt", s_data_str.join("\n"))
            .expect("Unable to write to s_data.txt");
    }
}

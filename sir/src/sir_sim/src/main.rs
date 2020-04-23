pub mod generator;

fn main() {
    let mut generator: generator::Generator = generator::Generator::new(300, 75000, 0.0009);
    generator.sir_trials();
    // generator.write_data();
    println!("{:?}", generator.s_set);
    println!("{:?}", generator.i_set);
    println!("{:?}", generator.r_set);
}

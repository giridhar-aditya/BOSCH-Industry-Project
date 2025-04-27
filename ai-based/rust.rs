use std::io;


struct FortuneMachine{

fn fortune1(){
println!("Fortune #1: A new opportunity is coming your way!");
    }
fn fortune2(){
println!("Fortune #2: Someone will bring you good news today.");
    }
fn fortune3(){
println!("Fortune #3: You will find what you've been looking for.");
    }
fn fortune4(){
println!("Fortune #4: Trust your instincts—they won't fail you.");
    }
fn fortune5(){
println!("Fortune #5: A small act of kindness will come back to you.");
    }
fn fortune6(){
println!("Fortune #6: You will laugh a lot today—enjoy it!");
    }
fn fortune7(){
println!("Fortune #7: Challenges will make you stronger.");
    }
fn fortune8(){
println!("Fortune #8: You are closer to success than you think.");
    }
fn fortune9(){
println!("Fortune #9: Good things take time—be patient.");
    }
fn fortune10(){
println!("Fortune #10: Your energy is magnetic today!");
    }
fn unknownFortune(){
println!("Invalid number! Pick between 1 and 10.");
    }
};

fn showMoodMenu(){
println!("\nHow are you feeling today?\n");
println!("1. Happy\n");
println!("2. Sad\n");
println!("3. Excited\n");
println!("4. Tired\n");
println!("5. Curious\n");
println!("Choose your mood (1-5): ");
}

fn reactToMood(){
if mood==1{
println!("Nice! Let's make your day even better!\n");
if mood==2{
println!("Cheer up! Here's something for you.\n");
if mood==3{
println!("Awesome energy! Let's keep it going.\n");
if mood==4{
println!("You deserve a break. Have a peaceful fortune.\n");
if mood==5{
println!("Curiosity brings rewards. Let's see your fortune.\n");
std::::::<>()
println!("That's not a valid mood. But let's continue!\n");
    }
}

fn main(){
    FortuneMachine fm;
let mood:i16;let number=1;let again=1;
println!("====== Fortune Cookie Machine ======\n");
while again==1{
        showMoodMenu();
let mut mood=String::new();std::io::stdin().read_line(&mut mood).unwrap();
        reactToMood(mood);
println!("\nPick a number between 1 and 10: ");
let mut number=String::new();std::io::stdin().read_line(&mut number).unwrap();
if number==1{
            fm.fortune1();
if number==2{
            fm.fortune2();
if number==3{
            fm.fortune3();
if number==4{
            fm.fortune4();
if number==5{
            fm.fortune5();
if number==6{
            fm.fortune6();
if number==7{
            fm.fortune7();
if number==8{
            fm.fortune8();
if number==9{
            fm.fortune9();
if number==10{
            fm.fortune10();
std::::::<>()
            fm.unknownFortune();
        }
println!("\nWould you like another fortune? (1 = Yes, 0 = No): ");
let mut again=String::new();std::io::stdin().read_line(&mut again).unwrap();
println!("You chose :",again);
    }
println!("\nThanks for using the Fortune Cookie Machine. Goodbye!\n");
return 0;
}
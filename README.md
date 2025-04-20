<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Robijn98/autoRig">
    <img src="images/dragonRig.png" alt="Logo" width="250">
  </a>
  <h3 align="center">Rig Forge Tool</h3>
  
</div>

## Built With
<div align="center">

[![Linux](https://img.shields.io/badge/platform-Linux-green?logo=linux&logoColor=white)](#)
[![Maya](https://img.shields.io/badge/platform-Maya-blue?logo=autodesk&logoColor=white)](#)
[![Python](https://img.shields.io/badge/platform-Python-blue?logo=python&logoColor=white)](#)

</div>


<!-- ABOUT THE PROJECT -->
### About The Project

RF is a tool you can use within maya to autorig creatures and digidoubles. The tool uses a skeleton
to build upon and creates all controllers and functionality through a modifiable script. 



<!-- GETTING STARTED -->
## Getting Started
### Prerequisites

To run you will need the following 
- python 
- maya2023

### Installation
Clone the repo
   ```sh
   git clone https://github.com/Robijn98/autoRig.git
   ```

## Usage

To use RT I would recommend creating a link between your code editor of choice and maya. 
To run the different functions you will need a prebuild skeleton that uses the suffix _JNT. 
Build a main that uses all of the functions you desire in your rig and run it. If you have 
a rig previously built using this system you can chose to re-use the controllers built, if you don't
built the controller and use the extract_curve_data function and save_curve_to_json to create a json file
that will preserve this information for you so you can go back and adjust main in any way while perserving
your curves, creating a non-destructive workflow. 

> [!WARNING]  
> This system was built to suit my personal needs and might not work for you

<!-- ROADMAP -->
## Roadmap 
- [x] Create base digidouble style rig
- [x] Create baseface (fleshy eye and zipper mouth) 
- [x] Resusable controllers
- [x] Stretch limbs
- [ ] Autocreate main file for each new character through a command in maya
- [ ] Autoskinning
- [ ] Better tail system
- [ ] Wing system

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

madhav Shyam and Sasha Ciolac 

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from metastablex.physics.engine import MetastableXEngine
from metastablex.physics.potentials import (
    ginzburg_landau,
    epidemic_potential,
    market_potential,
    physiological_potential
)

st.set_page_config(
    page_title="MetastableX Complex Systems Simulator",
    layout="wide"
)

st.title("⚛️ MetastableX Complex Systems Simulator")

system = st.sidebar.selectbox(
    "System",
    ["Ising-like Physics", "Epidemiology", "Financial Market", "Physiology"]
)

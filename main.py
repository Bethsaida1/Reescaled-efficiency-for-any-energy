import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#EN LA LÍNEA 54 SE DEBE INCLUIR MANUALMENTE LA DISTANCIA DESDE EL DETECTOR HASTA LA MUESTRA

# Definir la energía para la cual me interesa la eficiencia:
todas_E = np.array([140.1781, 171.8451, 188.1783, 196.3095, 202.642, 225.8766, 229.9301, 243.2803, 245.8648, 245.9131, 319.9865, 374.4953, 387.9538, 395.4384, 479, 486.3853, 495.8068, 553.832, 558.4747, 563.5337, 604.2856, 618.7066, 685.1772, 697.6765, 775.5327, 826.9455, 888.6332, 1043.3542, 1075.9988, 1098.5061, 1291.1098, 1316.9996, 1368.0524, 1474.1206, 1524.0377, 1595.6841, 2242.341])

#E = todas_E[23]
E = 1119.5044

# Datos proporcionados
x_data = np.array([5.8, 20, 50, 100, 150])
#y_data = np.array([7.0324, 0.9704, 0.0437, 0.0437, 0.0200]) #valores incorrectos usados antes
#y_data = np.array([7.1328, 1.0000, 0.1764, 0.0450, 0.0206]) #valores correctos usados después. Ahora no se copian y pegan los valores de excel, sino que aquí mismo se calculan las eficiencias normalizadas

eff5_8 = np.exp(-0.0309960141089354*np.log(E)**4 + 0.746862801749932*np.log(E)**3 - 6.71807170186974*np.log(E)**2 + 26.0384025677827*np.log(E) - 39.3913632054138)

eff20 = np.exp(-0.0154394074713738*np.log(E)**4 + 0.39750374452704*np.log(E)**3 - 3.85504522142503*np.log(E)**2 + 16.0049049609804*np.log(E) - 28.8616742394248)

eff20 = np.exp(-0.0154394074713738*np.log(E)**4 + 0.39750374452704*np.log(E)**3 - 3.85504522142503*np.log(E)**2 + 16.0049049609804*np.log(E) - 28.8616742394248)

eff50 = np.exp(0.0063903853873754*np.log(E)**4 - 0.0980957287803471*np.log(E)**3 + 0.302753425513191*np.log(E)**2 + 0.777269106523096*np.log(E) - 10.1227818069034)

eff100 = np.exp(0.00510130134493464*np.log(E)**4 - 0.0653617509762632*np.log(E)**3 + 0.00219509070237338*np.log(E)**2 + 1.98272442674187*np.log(E) - 13.2898412577199)

eff150 = np.exp(0.0143219074091857*np.log(E)**4 - 0.276114560598572*np.log(E)**3 + 1.77064470736986*np.log(E)**2 - 4.46790562323633*np.log(E) - 5.45751499497828)

y_data = np.array([eff5_8/eff20, 1, eff50/eff20, eff100/eff20, eff150/eff20])

deff_eff = np.array([0.03, 0.0386, 0.0525, 0.0489, 0.052])

y_data_error = y_data*np.sqrt(deff_eff**2+0.0386**2)

# Definir la función de ajuste
def model(x, A, B):
    return A / (x - B)**2

# Adivinanza inicial
initial_guess = [513, -2.6] #estos son con los que obtuve los valores de los datos que está en excel
#initial_guess = [510, -2.6] #para las entradas 0 y 1
#initial_guess = [519, -2.8] #para la entrada 5
#initial_guess = [519, -2.8] #para la entrada 23

# Realizar el ajuste de curva
params, covariance = curve_fit(model, x_data, y_data, p0=initial_guess)

# Obtener los valores ajustados de A y B
A, B = params

# Calcular la incertidumbre en los parámetros (error estándar)
uncertainty_A = np.sqrt(covariance[0, 0])
uncertainty_B = np.sqrt(covariance[1, 1])

print(f"Parámetro A: {A} ± {uncertainty_A}")
print(f"Parámetro B: {B} ± {uncertainty_B}")

# Generar datos para la curva ajustada
x_fit = np.linspace(min(x_data), max(x_data), 100)
y_fit = model(x_fit, A, B)

eff_E = model(239, A, B)*eff20 #239 cm desde el detector

#incertidumbre en la eficiencia
d_eff_E = eff_E*np.sqrt((uncertainty_A/A)**2 + (uncertainty_B/B)**2 + 0.0386**2)

print(f"La eficiencia para {E}keV es {eff_E} {d_eff_E}")
#print(f"con incertidumbre de {d_eff_E}")

# Graficar los datos originales y la curva ajustada
plt.scatter(x_data, y_data, label='Calibration points', color='red')
plt.plot(x_fit, y_fit, label=f'Fit: y = {A:.4f}/(x + {-B:.4f})^2', color='blue')
plt.xlabel('x = Distance from the detector')
plt.ylabel('y = eff/eff20(196keV)')
plt.title(f'Normalized efficiency vs distances for {E}keV')
plt.legend()
plt.show()
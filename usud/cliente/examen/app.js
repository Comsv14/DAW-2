// Clase Persona: Representa a una persona con su nombre, peso y altura
class Persona {
    constructor(nombre, peso, altura) {
        this.nombre = nombre; // El nombre de la persona
        this.peso = peso; // El peso de la persona (en kg)
        this.altura = altura; // La altura de la persona (en metros)
    }

    // Método para calcular el Índice de Masa Corporal (IMC)
    calcularIMC() {
        return (this.peso / (this.altura ** 2)).toFixed(2); // Fórmula del IMC
    }

    // Método para obtener el estado según el IMC
    obtenerEstado() {
        const imc = parseFloat(this.calcularIMC()); // Convertir el IMC a número
        if (imc < 18.5) {
            return "delgada"; // IMC menor a 18.5
        } else if (imc >= 18.5 && imc <= 24.9) {
            return "normal"; // IMC entre 18.5 y 24.9
        } else {
            return "con sobrepeso"; // IMC mayor a 24.9
        }
    }
}

// Lista global para almacenar las personas
const personas = [];

// Función para añadir una persona
function agregarPersona(nombre, peso, altura) {
    if (altura > 3) {
        altura = altura / 100; // Convertir centímetros a metros si es necesario
    }

    if (nombre && peso > 0 && altura > 0) { // Validar datos
        const persona = new Persona(nombre, peso, altura); // Crear nueva persona
        personas.push(persona); // Añadir a la lista
        alert(`Persona añadida: ${nombre}`); // Mostrar mensaje de éxito
        mostrarPersonas(); // Actualizar la lista visible
    } else {
        alert("Por favor, introduce datos válidos."); // Mostrar mensaje de error
    }
}

// Función para modificar los datos de una persona existente
function modificarPersona(nombre, nuevoPeso, nuevaAltura) {
    if (nuevoPeso > 0 && nuevaAltura > 0) { // Validar datos
        const persona = personas.find(p => p.nombre === nombre); // Buscar por nombre

        if (persona) {
            if (nuevaAltura > 3) {
                nuevaAltura = nuevaAltura / 100; // Convertir centímetros a metros si es necesario
            }

            persona.peso = nuevoPeso; // Actualizar peso
            persona.altura = nuevaAltura; // Actualizar altura

            alert(`Datos actualizados para: ${nombre}`); // Mostrar mensaje de éxito
            mostrarPersonas(); // Actualizar la lista visible
        } else {
            alert(`No se encontró una persona con el nombre: ${nombre}`); // Mostrar error si no existe
        }
    } else {
        alert("Por favor, introduce valores válidos para peso y altura."); // Mostrar mensaje de error
    }
}

// Función para mostrar todas las personas en la lista HTML
function mostrarPersonas() {
    const lista = document.getElementById("listaPersonas"); // Obtener la lista
    lista.innerHTML = ""; // Limpiar la lista actual

    personas.forEach(persona => {
        const item = document.createElement("li"); // Crear un nuevo elemento
        item.textContent = `${persona.nombre}: Peso = ${persona.peso}kg, Altura = ${persona.altura}m`; // Texto de la persona
        lista.appendChild(item); // Añadir a la lista visible
    });
}

// Función para calcular y mostrar el IMC de todas las personas
function mostrarIMC() {
    if (personas.length > 0) { // Comprobar si hay personas
        const resultados = personas.map(persona => {
            // Generar mensaje con IMC y estado
            return `${persona.nombre}: IMC = ${persona.calcularIMC()}, Estado = ${persona.obtenerEstado()}`;
        });
        alert(resultados.join("\n")); // Mostrar resultados en una alerta
    } else {
        alert("No hay personas registradas."); // Mostrar mensaje si no hay personas
    }
}

// Conexión con los botones del formulario
document.getElementById("Agregar").addEventListener("click", () => {
    const nombre = document.getElementById("nombre").value;
    const peso = parseFloat(document.getElementById("peso").value);
    const altura = parseFloat(document.getElementById("altura").value);
    agregarPersona(nombre, peso, altura); // Llamar a la función para agregar
});

document.getElementById("Modificar").addEventListener("click", () => {
    const nombre = document.getElementById("nombre").value;
    const nuevoPeso = parseFloat(document.getElementById("peso").value);
    const nuevaAltura = parseFloat(document.getElementById("altura").value);
    modificarPersona(nombre, nuevoPeso, nuevaAltura); // Llamar a la función para modificar
});

document.getElementById("Calcular").addEventListener("click", mostrarIMC); // Conectar botón de cálculoo

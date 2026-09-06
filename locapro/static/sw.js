self.addEventListener("install", (event) => {
    console.log("Service Worker: Instalado");
});
self.addEventListener("fetch", (event) => {
    // Permite que a rede lide com as requisições (não faz cache offline complexo agora)
});

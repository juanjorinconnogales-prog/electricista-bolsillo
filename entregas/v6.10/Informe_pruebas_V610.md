# Electricista en el Bolsillo V6.10 — informe verificable

**Estado: compilación y regresión verificadas; entrega neuronal bloqueada. No se declara la aplicación terminada.**

Fecha: 24 de octubre de 2026, zona Europe/Madrid. Los logs conservan UTC. Se utilizó el ZIP Electricista_V6_10_CODEX.zip como proyecto principal y se leyó su AGENTS.md. El ZIP original y el repositorio anterior se conservaron sin modificaciones en /workspace/work/. El proyecto actualizado se integra en /workspace/electricista-bolsillo.

## Resultado principal

- APK debug y AAB release compilados realmente con Gradle. El runtime LiteRT-LM y sus llamadas Kotlin/Java compilan; ambos artefactos contienen liblitertlm_jni.so para arm64-v8a y x86_64.
- El modelo Qwen3-0.6B.litertlm **no está presente**. Su descarga falló por HTTP 403 del proxy al destino huggingface.co. No se ha ejecutado generación de lenguaje con pesos entrenados y no se atribuye a reglas el carácter de inferencia neuronal.
- El HTML independiente conserva su biblioteca local. No puede ejecutar la clase Kotlin ni LiteRT-LM Android en Chrome. La interfaz informa del motor de reglas.
- Se verificó la conservación de los 254 símbolos, 1.014 referencias de catálogo, 160 identificadores de conocimiento y las APIs principales frente al HTML exacto del ZIP V6.10 original.

## Matriz de pruebas

| Prueba | Estado | Evidencia y alcance |
|---|---|---|
| assembleDebug | PASS | evidence/gradle-exact-model-final.log; APK real, firma debug comprobada |
| bundleRelease | PASS compilación | Mismo log; AAB sin firma de publicación y sin pesos; no apto para Play todavía |
| assembleDebugAndroidTest | PASS | APK instrumentada compilada con pruebas de OCR, WebView e inferencia |
| testDebugUnitTest | PASS | 5 tests JUnit, cero fallos; XML e informe HTML copiados a evidence/reports |
| lintDebug | PASS con avisos | Cero errores, cinco avisos. Informe completo incluido |
| Diagnóstico JS | PASS | 67 casos; mezcla de negaciones, averías y ES/EN/FR |
| Etapas JS | PASS | 12 casos de secuencia y preguntas |
| Vocabulario JS | PASS | 112 casos de sinónimos, sujetos y negaciones |
| Respuestas completas JS | PASS | 22 comprobaciones |
| Interfaz web heredada adaptada | PASS | 35 comprobaciones; planos, catálogo, importación/exportación, presupuestos y PDF |
| Comparación funcional con baseline V4.4 | PASS | IVA 0/10/21%, historial, PDF ES/EN/FR, calculadora, escáner guiado y diagnóstico |
| Seguridad y funcionamiento web V6.10 | PASS | 11 emergencias ES/EN/FR, botones IA superior e inferior, modo offline, cálculo contrastado e inputs inválidos |
| Conservación de datos/API V6.10 | PASS | evidence/v610-preservation.json; comparación contra el ZIP original, sin usar resultados históricos como prueba actual |
| OCR ML Kit en Android sin red | PASS repetición final | Texto real reconocido: C16 230V 30mA; generado como píxeles y procesado por ML Kit |
| Pesos ausentes en Android | PASS repetición final | El motor devuelve error y nunca éxito neuronal |
| WebView Android, primera ejecución | FAIL detectado y corregido en código | WebView 83: sintaxis PDF.js y métodos replaceChildren/at no disponibles; además timeout en entorno sin aceleración |
| Repetición Android con correcciones | PASS: 3 aprobadas / 1 SKIP | WebView, presupuesto, seguridad, 254 símbolos y PDF; OCR; error honesto sin pesos. Inferencia omitida por ausencia de modelo. evidence/android-final-results.json |
| Descarga de pesos | BLOCKED | evidence/model-install-attempt.log y model-network.log, HTTP 403 |
| Rechazo de importación local incompleta | PASS | Test JUnit y prueba Python; el fichero incompleto se rechaza antes de cargar o reemplazar pesos |
| Compatibilidad del modelo completo con el runtime | SKIP | No hay archivo auténtico disponible para inicializar Engine |
| Integridad de pesos reales | SKIP | No existe archivo descargado: tamaño y SHA256 reales no disponibles |
| Inferencia generativa offline con pesos entrenados | SKIP | Falta modelo. El test instrumentado se omite expresamente; no se sustituye por pesos aleatorios |
| ARM64 físico, RAM y latencia generativa | SKIP | No hay dispositivo ARM64 ni pesos ejecutables disponibles |
| Cámara real, permisos de aplicaciones externas y compartir/imprimir físicamente | SKIP | Sin hardware ni aplicaciones receptoras físicas; contratos de bytes PDF sí probados en navegador |
| Clasificador eléctrico especializado | SKIP | No se recibió electrical_classifier.tflite ni dataset validado. OCR y candidato geométrico no prueban identificación eléctrica |
| Play Asset Delivery instalado desde Google Play | SKIP | El asset pack compila, pero no se publicó ni instaló desde Play |
| release_gate.py | BLOQUEO CORRECTO | Exit 2 por pesos/evidencia ausentes; impide declarar preparada la entrega neuronal |

Las suites web se ejecutan contra los archivos actuales. Los informes antiguos recibidos en pruebas/historico_versiones_anteriores se conservan únicamente como antecedentes. Los tests adaptados mantienen nombres V4.5 por procedencia; sus datos esperados se actualizaron a V6.10 cuando eran cantidades antiguas (124→254 símbolos, 774→1.014 referencias). Las comprobaciones de unicidad, vectores, aritmética, persistencia y errores permanecen.

## Errores corregidos

1. **Java/Kotlin con destinos JVM diferentes:** Java 17 frente a Kotlin 21 causaba compileDebugKotlin FAILED. app/build.gradle fija jvmTarget 17 para Kotlin y conserva Java 17.
2. **Atrás en Android 16:** lint detectaba GestureBackNavigation. MainActivity usa ComponentActivity y OnBackPressedDispatcher; conserva volver por el historial de WebView y cerrar si no hay historial.
3. **Estilo incompatible con API 24:** windowLightNavigationBar requiere API 27. El atributo pasa a res/values-v27; se mantiene minSdk 24.
4. **Falso éxito neuronal para emergencias:** el puente nativo devolvía true para texto fijo. Ahora utiliza fuente safety y éxito neuronal false; el HTML no lo etiqueta como generación. neuralModelLoaded permanece false hasta un resultado real completado; presencia y carga son conceptos separados.
5. **Negación que ocultaba un peligro:** «no hay humo pero hay chispas» y la variante inversa descartaban todo el riesgo. Ahora se evalúa evidencia por cláusula; los casos positivos y totalmente negados pasan.
6. **Seguridad por rutas:** ElectricalSafety se comparte entre ambos asistentes nativos; la ruta web utiliza el mismo vocabulario conservador, incluyendo electrocución, calambre y términos EN/FR. Se mejoró la definición nativa de contactor y se conserva la prioridad de emergencias.
7. **WebView antiguo:** el emulador reveló errores de parser PDF.js y APIs DOM/Array. Se incluyen core-js y un polyfill de replaceChildren; ambos módulos PDF.js se transforman a sintaxis Chrome 83 con esbuild. Los módulos originales y licencias se conservan. La reconstrucción repetida produce el mismo SHA256; las ocho suites web pasan tras el cambio. La repetición nativa final también aprobó carga de PDF.js y parseo del PDF generado.
8. **Importación de pesos sin integridad:** tanto instalación por Python como importación/descarga nativa exigen el SHA256 fijado. El instalador ya no considera válido un archivo solo por su tamaño y utiliza reemplazo atómico. No se cambió el pin para aceptar un artefacto desconocido.
9. **Exportación CSV bloqueada en Android:** el puente solo admitía PDF/JSON, aunque el catálogo exportaba CSV. Ahora admite el MIME CSV y conserva límites, nombres saneados y contratos de guardado.
10. **Cámara y visibilidad de paquetes:** se añadió queries para ACTION_IMAGE_CAPTURE, necesario para resolver la cámara en Android 11+.

La cabecera y la navegación inferior mantienen ambos accesos al asistente; el superior permanece en el flujo del documento, sin botón flotante que cubra campos. Los tests comprueban ambos accesos.

## Runtime y modelo

Runtime elegido: com.google.ai.edge.litertlm:litertlm-android:0.18.0. La dependencia se descargó de Google Maven. Se contrastaron las firmas con el AAR y el código oficial del tag v0.18.0; no se inventaron métodos. EngineConfig, Backend.CPU, ConversationConfig, sendMessageAsync y cancelProcess compilan con esa versión.

La integración usa un trabajador serial, un límite de contexto de 2.048 tokens y un máximo de 384 tokens por respuesta. Crea un contexto nuevo por consulta, evita una cola ilimitada, permite cancelación y cierra recursos. El watchdog responde a los 120 segundos; una inicialización nativa bloqueada no se puede terminar de forma segura a la fuerza, por lo que el motor puede seguir ocupado hasta retornar. Reemplazar un modelo exige esperar el cierre. Estas rutas compilan; su comportamiento con pesos reales, cancelación en plena inferencia y presión de memoria sigue sin verificarse.

Se recupera orientación local por tema mediante OfflineElectricalAssistant y se incorpora al contexto del modelo. Es recuperación determinista básica, no búsqueda vectorial ni entrenamiento especializado. El contexto no se presenta como norma certificada. Hay instrucciones de seguridad y un filtro conservador de salida; no se garantiza que detecten todo consejo peligroso.

Modelo previsto: Qwen3-0.6B convertido a .litertlm. URL intentada:

https://huggingface.co/litert-community/Qwen3-0.6B/resolve/main/Qwen3-0.6B.litertlm

Tamaño exacto esperado, confirmado por el usuario: **613722264 bytes**. Este es un requisito de validación, no una medición de un archivo descargado aquí. Pin del proyecto, también confirmado expresamente por el usuario: c5f39b4191926786c3e6668b62af4d6eb15248dfc7a5348252a9b406f33f2108. **No se pudo confirmar independientemente contra metadatos remotos.** El SHA calculado de un archivo real y su tamaño no se inventan: constan como null en MODEL_MANIFEST.json.

El README oficial de Qwen3 declara Apache-2.0 para sus modelos abiertos y remite a Hugging Face y ModelScope. La documentación oficial LiteRT-LM remite a Hugging Face para modelos convertidos. No se encontró una distribución verificable y entrenada equivalente en los destinos permitidos. El repositorio oficial de LiteRT-LM sí contiene test_lm.litertlm; su propio conversation_test.cc explica que usa pesos aleatorios y genera texto sin sentido. Se descartó como sustituto y nunca se instaló en la app. No se eludieron las restricciones del proxy.

No hay medidas de RAM ni latencia generativa. Qwen3 0.6B tiene aproximadamente 0,3 GB de pesos a 4 bits o 0,6 GB a 8 bits como orden de magnitud teórico, antes de metadatos, caché y runtime; no son tamaños descargados ni consumo total medido. Una alternativa pequeña como SmolLM2 135M requeriría otra conversión/runtime y validación de calidad; no hay artefacto compatible verificado disponible aquí. No se promete viabilidad en gama media sin medirla.

Distribución: AAB con pack neuralmodel install-time para Play; APK manual mediante importación privada del Qwen3 validado. La inspección de los artefactos entregados confirma ausencia de .litertlm. El AAB no contiene firma de publicación y no se subió a ningún servicio.

## Reproducción y evidencias

Compilación real ejecutada:

```
./gradlew --no-daemon assembleDebug bundleRelease assembleDebugAndroidTest testDebugUnitTest lintDebug
```

Entorno: Linux x86_64, JDK OpenJDK 21.0.12.1 completo, JVM destino 17, Gradle 8.13, AGP 8.13.2, Kotlin 2.3.20, SDK 36 / build tools 36.0.0. Para respetar las carpetas escribibles se situaron SDK, Gradle y configuración Android bajo /workspace/work. El proxy se configuró por propiedades Java conservando verificación TLS. No se incluyen credenciales ni keystores en el proyecto.

```
python pruebas/run_web_tests.py
python instalar_modelo_oficial.py
python release_gate.py
```

En este entorno se utilizó Chromium del sistema y Playwright 1.57.0. La suite sirve únicamente 127.0.0.1 y registra solicitudes externas; la prueba específica desactiva la conectividad del navegador tras cargar el HTML local. No encontró errores JS ni solicitudes HTTP externas en las ejecuciones aprobadas.

Emulador: Android 11 / API 30 x86_64, WebView 83.0.4103.120, sin /dev/kvm, con traducción por software. Primera ejecución con 2.048 MiB; repetición con 1.536 MiB. La primera ejecución aprobó OCR y pesos ausentes, omitió inferencia y falló WebView. Se conservaron los logs del fallo y se corrigieron los errores de compatibilidad. El emulador sufrió además lentitud, ANR de System UI y finalización del proceso con exit 137; esos fallos de entorno no se presentan como aprobados. La repetición final figura en evidence/device-exact-metadata-final.log y evidence/instrumentation-results.log: 52,005 segundos, tres tests aprobados y uno omitido (-4: inferencia sin pesos). El mensaje JUnit «OK (4 tests)» incluye esa omisión; no son cuatro aprobados. La prueba del PDF necesitó partir de un plano vacío, porque la plantilla inicial exige confirmación antes de reemplazarse; se corrigió el fixture del test, sin eliminar la protección de la aplicación. El aviso «Setting up fake worker» es de PDF.js: el parser real se ejecuta en el hilo principal, no representa inferencia neuronal ni una simulación de ella. La captura android-after-systemui-wait.png muestra la aplicación tras pulsar «Wait» de forma automatizada; android-systemui-anr.png conserva el ANR del System UI del emulador: las aserciones programáticas pasan, pero no se certifica fluidez ni estabilidad del sistema en ese emulador sin aceleración.

Consultar evidence/artifact-inspection.json para SHA256 de APK/AAB y comprobación de igualdad exacta del HTML empaquetado. evidence/apk-signature.log verifica firma de desarrollo. evidence/reports contiene JUnit y lint. Los PDFs y capturas de regresión se conservan junto a los resultados actuales.

Los cinco avisos de lint restantes son: versión posterior de coroutines disponible, JavaScript habilitado (requerido por la app y con recursos remotos bloqueados en WebView), dataExtractionRules, falta de icono explícito y versión posterior de Activity disponible. El listado concreto vigente se conserva en el informe de lint; no se silenció ningún error.

## Criterio de aceptación

Faltan pesos entrenados, verificación de su procedencia y licencia de conversión, inferencia real offline, medidas en ARM64 y las comprobaciones físicas indicadas. Las pruebas instrumentadas finales de WebView/PDF, OCR y pesos ausentes han pasado con el dispositivo sin red. El proyecto queda preparado para continuar y contiene la prueba real, que exige hash correcto y ausencia de red antes de generar; solo entonces escribe neural-evidence.json con entrada, salida, duración y memoria observada. release_gate.py continúa bloqueando publicación. No se declara el trabajo neuronal completado ni se sustituye por una demostración simulada.

## Ubicación de entrega

Los archivos se guardan en /workspace/output. La ruta /codex/.../output indicada por el cliente no existe en el contenedor seleccionado y su creación falla por permisos de la raíz. No hay una herramienta de adjuntos duraderos en esta sesión; no se inventan enlaces de descarga. El proyecto actualizado también queda en /workspace/electricista-bolsillo.

## Actualización: metadatos exactos e importación local

Se mantiene LiteRT-LM 0.18.0. ModelIntegrity.java centraliza tamaño exacto (613722264 bytes) y SHA256. Se aplica al selector de archivos, a la descarga integrada y de nuevo al inicio de Engine, antes de cargar pesos desde el asset pack o almacenamiento privado. La presencia solo se anuncia si el archivo tiene el tamaño esperado; esto no certifica su hash ni inferencia hasta que el trabajador los comprueba. No se permite sustituir el archivo previo con una importación inválida.

El instalador Python incorpora --from-file para una importación local totalmente offline. La comprobación de publicación y release_gate utilizan la misma verificación exacta. Los tests rechazan una entrada incompleta .bin; no se crearon pesos .litertlm falsos. La prueba positiva de tamaño/hash con el archivo completo, su carga y la inferencia permanecen SKIP. La URL facilitada por el usuario se comprobó de nuevo y el proxy sigue devolviendo HTTP 403; evidencia: model-network-latest.log.

Para continuar la inferencia automatizada aquí, el archivo auténtico debe estar disponible, por ejemplo, en /workspace/Qwen3-0.6B.litertlm. Con él se podrá ejecutar el instalador local y el test real preparado. No basta con disponer de la URL y los metadatos.

## Costes

No se han efectuado compras, contratado servicios, activado facturación ni usado APIs comerciales de inferencia. La compilación y verificación finales completas se ejecutan con Gradle --offline sobre dependencias ya descargadas (gradle-exact-model-final.log). Las pruebas utilizan únicamente el entorno existente y herramientas gratuitas. No se pueden inspeccionar las condiciones comerciales de la cuenta: no se afirma ni modifica su facturación. Se deja la prohibición expresa de gastos en AGENTS.md para todo el proyecto, incluida V6 PRO.

## Ollama FAQ

### Creating Custom Models
Create a model to:
- edit [parameters](https://github.com/ollama/ollama/blob/main/docs/modelfile.md#valid-parameters-and-values) of an already existing model
- import [safetensor / gguf models](https://github.com/ollama/ollama/blob/main/docs/modelfile.md#build-from-a-safetensors-model) not from ollama

Ollama can create custom models. For both cases, you need a Modelfile - which is simply a text file that must be named "Modelfile" (without .txt)

#### Modelfile to edit temperature of a model
```
FROM <base-model>:<tag>
PARAMETER temperature 0
```

The `FROM` instruction tells ollama what base model to use, the `PARAMETER` of `temperature 0` tells the model, to strictly use prediction with the highest probabilities (=> reproducible), whereas a higher temperature (default is 0.7) makes the model less predictable and more creative.


#### Create Custom Model from Modelfile
```bash
ollama create -f <path to your Modelfile> <name of your custom model>

# use model
ollama run <name of your custom model>
```

Example:
```bash
ollama create -f ollama/custom-models/qwen-2-5-7b-repr/Modelfile qwen2.5-7b-repr

ollama run qwen2.5-7b-repr
```


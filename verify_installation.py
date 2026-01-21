"""
Installation Verification Script for HeartMuLa GUI
Checks all dependencies and CUDA availability
"""

import sys
import os

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def check_python_version():
    print_section("Python Version")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor == 10:
        print("✓ Python 3.10 detected (CORRECT)")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor} detected")
        print("⚠ WARNING: Python 3.10 is required!")
        return False

def check_torch():
    print_section("PyTorch")
    try:
        import torch
        print(f"✓ PyTorch version: {torch.__version__}")
        
        # Check CUDA
        if torch.cuda.is_available():
            print(f"✓ CUDA is available")
            print(f"  CUDA version: {torch.version.cuda}")
            print(f"  Device count: {torch.cuda.device_count()}")
            print(f"  Current device: {torch.cuda.current_device()}")
            print(f"  Device name: {torch.cuda.get_device_name(0)}")
            
            # Check memory
            total_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
            print(f"  Total VRAM: {total_memory:.2f} GB")
            return True
        else:
            print("✗ CUDA is NOT available")
            print("⚠ ERROR: Torch not compiled with CUDA enabled")
            print("\nTo fix:")
            print("1. Delete the venv folder")
            print("2. Run setup_gui.bat again")
            print("3. It will install CUDA-enabled PyTorch")
            return False
            
    except ImportError:
        print("✗ PyTorch not installed")
        return False

def check_triton():
    print_section("Triton")
    try:
        import triton
        print(f"✓ Triton version: {triton.__version__}")
        return True
    except ImportError:
        print("✗ Triton not installed")
        print("⚠ WARNING: Triton may be required for optimal performance")
        return False

def check_transformers():
    print_section("Transformers")
    try:
        import transformers
        print(f"✓ Transformers version: {transformers.__version__}")
        return True
    except ImportError:
        print("✗ Transformers not installed")
        return False

def check_bitsandbytes():
    print_section("BitsAndBytes (FP8 Support)")
    try:
        import bitsandbytes as bnb
        print(f"✓ BitsAndBytes version: {bnb.__version__}")
        print("✓ FP8 quantization available")
        return True
    except ImportError:
        print("✗ BitsAndBytes not installed")
        print("⚠ WARNING: FP8 quantization will not be available")
        print("Install with: pip install bitsandbytes")
        return False

def check_other_deps():
    print_section("Other Dependencies")
    deps = {
        'tokenizers': 'Tokenizers',
        'torchaudio': 'TorchAudio',
        'accelerate': 'Accelerate',
        'scipy': 'SciPy',
        'numpy': 'NumPy',
        'tqdm': 'TQDM',
    }
    
    all_ok = True
    for module, name in deps.items():
        try:
            mod = __import__(module)
            version = getattr(mod, '__version__', 'unknown')
            print(f"✓ {name}: {version}")
        except ImportError:
            print(f"✗ {name}: not installed")
            all_ok = False
    
    return all_ok

def check_tkinter():
    print_section("GUI Support")
    try:
        import tkinter
        print(f"✓ Tkinter available (GUI will work)")
        return True
    except ImportError:
        print("✗ Tkinter not available")
        print("⚠ ERROR: GUI cannot run without tkinter")
        return False

def check_model_files():
    print_section("Model Files")
    model_path = "./ckpt"
    
    required_files = [
        "HeartCodec-oss",
        "HeartMuLa-oss-3B",
        "gen_config.json",
        "tokenizer.json"
    ]
    
    if not os.path.exists(model_path):
        print(f"✗ Model directory not found: {model_path}")
        print("\nTo download models:")
        print("hf download --local-dir './ckpt' 'HeartMuLa/HeartMuLaGen'")
        print("hf download --local-dir './ckpt/HeartMuLa-oss-3B' 'HeartMuLa/HeartMuLa-oss-3B'")
        print("hf download --local-dir './ckpt/HeartCodec-oss' 'HeartMuLa/HeartCodec-oss'")
        return False
    
    all_ok = True
    for item in required_files:
        path = os.path.join(model_path, item)
        if os.path.exists(path):
            print(f"✓ {item}")
        else:
            print(f"✗ {item} - NOT FOUND")
            all_ok = False
    
    return all_ok

def check_output_folder():
    print_section("Output Folder")
    output_path = "./output"
    
    if os.path.exists(output_path):
        print(f"✓ Output folder exists: {output_path}")
    else:
        print(f"⚠ Output folder will be created: {output_path}")
        try:
            os.makedirs(output_path, exist_ok=True)
            print(f"✓ Created output folder")
        except Exception as e:
            print(f"✗ Failed to create output folder: {e}")
            return False
    
    return True

def main():
    print("\n" + "="*60)
    print("  HeartMuLa GUI - Installation Verification")
    print("="*60)
    
    results = {
        "Python 3.10": check_python_version(),
        "PyTorch + CUDA": check_torch(),
        "Triton": check_triton(),
        "Transformers": check_transformers(),
        "BitsAndBytes": check_bitsandbytes(),
        "Other Dependencies": check_other_deps(),
        "Tkinter": check_tkinter(),
        "Model Files": check_model_files(),
        "Output Folder": check_output_folder(),
    }
    
    print_section("Summary")
    
    critical_checks = ["Python 3.10", "PyTorch + CUDA", "Transformers", "Tkinter"]
    optional_checks = ["Triton", "BitsAndBytes", "Model Files"]
    
    critical_passed = all(results[check] for check in critical_checks if check in results)
    
    print("\nCritical Components:")
    for check in critical_checks:
        status = "✓ PASS" if results.get(check, False) else "✗ FAIL"
        print(f"  {status} - {check}")
    
    print("\nOptional Components:")
    for check in optional_checks:
        status = "✓ PASS" if results.get(check, False) else "⚠ MISSING"
        print(f"  {status} - {check}")
    
    print("\n" + "="*60)
    
    if critical_passed:
        print("✓ ALL CRITICAL CHECKS PASSED")
        print("\nYou can now run the GUI with: start.bat")
        
        if not results.get("BitsAndBytes", False):
            print("\n⚠ Note: FP8 quantization not available")
            print("  Install with: pip install bitsandbytes")
        
        if not results.get("Model Files", False):
            print("\n⚠ Note: Models not downloaded yet")
            print("  Download before using the GUI")
    else:
        print("✗ SOME CRITICAL CHECKS FAILED")
        print("\nPlease fix the issues above before running the GUI")
        print("\nRecommended action:")
        print("1. Delete the venv folder")
        print("2. Run setup_gui.bat")
        print("3. Run this verification script again")
    
    print("="*60 + "\n")
    
    return 0 if critical_passed else 1

if __name__ == "__main__":
    sys.exit(main())

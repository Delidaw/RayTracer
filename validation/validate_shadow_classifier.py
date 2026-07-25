import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from rendering.shadow_classifier import ShadowClassifier

classifier = ShadowClassifier()

captured = {
    "captured": True
}

escaped = {
    "captured": False
}

print(classifier.is_shadow(captured))
print(classifier.is_shadow(escaped))
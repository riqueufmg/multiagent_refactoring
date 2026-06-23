import xml.etree.ElementTree as ET
from typing import List, Tuple

class Dependencies:
    def __init__(self, target_fqn: str):
        self.target_fqn = target_fqn
    
    @staticmethod
    def is_test_class(fqn: str) -> bool:
        return fqn.endswith("Test") or ".test." in fqn.lower()

    def _get_package_dependencies(self, graphml_path: str) -> Tuple[List[str], List[str]]:
        ns = {"g": "http://graphml.graphdrawing.org/xmlns"}

        tree = ET.parse(graphml_path)
        root = tree.getroot()

        internal_edges, outgoing_edges, incoming_edges = [], [], []

        target_package = self.target_fqn

        for edge in root.findall(".//g:edge", ns):
            source = edge.get("source")
            target = edge.get("target")

            if not source or not target:
                continue

            if self.is_test_class(source) or self.is_test_class(target):
                continue
            
            if self._get_package_name(source) == target_package and self._get_package_name(target) == target_package:
                internal_edges.append((source, target))
            elif self._get_package_name(source) == target_package:
                outgoing_edges.append((source, target))
            elif self._get_package_name(target) == target_package:
                incoming_edges.append((source, target))

        return internal_edges, outgoing_edges, incoming_edges

    def _get_package_name(self, fqn: str) -> str:
        parts = fqn.split(".")
        if parts and parts[-1][:1].isupper():
            return ".".join(parts[:-1])
        return fqn

#target_fqn = "org.jsoup.integration"
#file = "data/DependencyGraph.graphml"

#deps = Dependencies(target_fqn)
#internal, outgoing, incoming = deps._get_package_dependencies(file)

#print(f"Internal Dependencies for {target_fqn}:")
#for dep in internal:
#    print(f"  {dep}")
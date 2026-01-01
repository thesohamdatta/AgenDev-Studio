from datetime import datetime

class TraceabilityMatrix:
    def __init__(self):
        self.matrix = {}  # {artifact_id: {upstream_id: ..., type: ...}}

    def link(self, upstream_id: str, downstream_id: str, relationship="generates"):
        if downstream_id not in self.matrix:
            self.matrix[downstream_id] = []
        self.matrix[downstream_id].append({
            "upstream": upstream_id,
            "type": relationship,
            "timestamp": datetime.utcnow().isoformat()
        })

    def get_lineage(self, artifact_id):
        """Recursively retrieve the lineage of an artifact."""
        lineage = []
        current = artifact_id
        while current in self.matrix:
            parent_link = self.matrix[current][0] # Simple linear lineage for now
            lineage.append(parent_link)
            current = parent_link['upstream']
        return lineage

trace_matrix = TraceabilityMatrix()

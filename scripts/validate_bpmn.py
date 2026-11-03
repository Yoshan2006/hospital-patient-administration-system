"""Structural checks for the HPAS design-only BPMN 2.0 files; stdlib only.

Checks are not a replacement for full BPMN XSD/editor validation.
"""
from collections import defaultdict, deque
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
NS={
 'bpmn':'http://www.omg.org/spec/BPMN/20100524/MODEL',
 'bpmndi':'http://www.omg.org/spec/BPMN/20100524/DI',
 'dc':'http://www.omg.org/spec/DD/20100524/DC',
 'di':'http://www.omg.org/spec/DD/20100524/DI',
}
q=lambda s: '{%s}%s'%(NS[s.split(':')[0]],s.split(':')[1])
FLOW_NODES={'startEvent','endEvent','task','userTask','serviceTask','exclusiveGateway'}

def validate(path):
 tree=ET.parse(path);root=tree.getroot()
 assert root.tag==q('bpmn:definitions')
 all_elements={el.attrib['id']:el for el in root.iter() if 'id' in el.attrib}
 assert len(all_elements)==len({el.attrib['id'] for el in root.iter() if 'id' in el.attrib}), 'duplicate ID'
 processes=root.findall('bpmn:process',NS);collabs=root.findall('bpmn:collaboration',NS)
 assert len(processes)==1 and len(collabs)==1
 process=processes[0];collab=collabs[0]
 assert process.attrib.get('isExecutable')=='false', 'must be non-executable'
 nodes={el.attrib['id']:el for el in process if el.tag.split('}')[-1] in FLOW_NODES}
 assert nodes
 starts={nid for nid,n in nodes.items() if n.tag==q('bpmn:startEvent')}
 ends={nid for nid,n in nodes.items() if n.tag==q('bpmn:endEvent')}
 assert starts and ends
 flows=process.findall('bpmn:sequenceFlow',NS)
 incoming=defaultdict(set);outgoing=defaultdict(set)
 for f in flows:
  src=f.attrib['sourceRef'];dst=f.attrib['targetRef'];fid=f.attrib['id']
  assert src in nodes and dst in nodes, f'bad sequence flow {fid}: {src}->{dst}'
  outgoing[src].add(fid);incoming[dst].add(fid)
 for nid,node in nodes.items():
  declared_in={e.text for e in node.findall('bpmn:incoming',NS)}
  declared_out={e.text for e in node.findall('bpmn:outgoing',NS)}
  assert declared_in==incoming[nid], f'incoming mismatch: {nid}'
  assert declared_out==outgoing[nid], f'outgoing mismatch: {nid}'
  if nid not in starts:assert incoming[nid],f'unreachable entry {nid}'
  if nid not in ends:assert outgoing[nid],f'dead end {nid}'
 # Reachability from starting events
 adj=defaultdict(list)
 for f in flows: adj[f.attrib['sourceRef']].append(f.attrib['targetRef'])
 queue=deque(starts);seen=set(starts)
 while queue:
  for next_id in adj[queue.popleft()]:
   if next_id not in seen:seen.add(next_id);queue.append(next_id)
 assert seen==set(nodes),f'unreachable nodes: {set(nodes)-seen}'
 # Lane ownership: exactly one lane per node
 owners=defaultdict(list)
 for lane in process.findall('.//bpmn:lane',NS):
  for child in lane.findall('bpmn:flowNodeRef',NS):owners[child.text].append(lane.attrib['id'])
 assert set(owners)==set(nodes)
 assert all(len(v)==1 for v in owners.values())
 # Participant and message flow references
 participant_ids={p.attrib['id'] for p in collab.findall('bpmn:participant',NS)}
 assert participant_ids
 for f in collab.findall('bpmn:messageFlow',NS):
  s=f.attrib['sourceRef'];t=f.attrib['targetRef']
  assert s in nodes or s in participant_ids
  assert t in nodes or t in participant_ids
  assert ((s in nodes) != (t in nodes)),f'message flow must cross pool boundary: {f.attrib["id"]}'
 # Graphical layout / importability in Camunda Modeler
 plane=root.find('bpmndi:BPMNDiagram/bpmndi:BPMNPlane',NS)
 assert plane is not None and plane.attrib['bpmnElement']==collab.attrib['id']
 rendered_shapes={shape.attrib['bpmnElement'] for shape in plane.findall('bpmndi:BPMNShape',NS)}
 rendered_edges={edge.attrib['bpmnElement'] for edge in plane.findall('bpmndi:BPMNEdge',NS)}
 assert set(nodes)|participant_ids <=rendered_shapes
 assert {f.attrib['id'] for f in flows}|{f.attrib['id'] for f in collab.findall('bpmn:messageFlow',NS)}<=rendered_edges
 for edge in plane.findall('bpmndi:BPMNEdge',NS):
  assert len(edge.findall('di:waypoint',NS))>=2,f'edge without waypoints: {edge.attrib["id"]}'
 return len(nodes),len(flows),len(collab.findall('bpmn:messageFlow',NS))

if __name__=='__main__':
 for name in ['outpatient-booking-notifications.bpmn','appointment-cancellation-dna.bpmn']:
  p=ROOT/'docs'/'bpmn'/name
  a,b,c=validate(p)
  print(f'PASS {name}: {a} nodes, {b} sequence flows, {c} message flows, BPMN DI present')
 print('NOTE: structural checks passed; also open both models in a BPMN 2.0 editor before assessment submission.')

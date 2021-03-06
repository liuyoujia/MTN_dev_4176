# script auto-generated by phenix.molprobity


from __future__ import absolute_import, division, print_function
from six.moves import cPickle as pickle
from six.moves import range
try :
  import gobject
except ImportError :
  gobject = None
import sys

class coot_extension_gui(object):
  def __init__(self, title):
    import gtk
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    scrolled_win = gtk.ScrolledWindow()
    self.outside_vbox = gtk.VBox(False, 2)
    self.inside_vbox = gtk.VBox(False, 0)
    self.window.set_title(title)
    self.inside_vbox.set_border_width(0)
    self.window.add(self.outside_vbox)
    self.outside_vbox.pack_start(scrolled_win, True, True, 0)
    scrolled_win.add_with_viewport(self.inside_vbox)
    scrolled_win.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

  def finish_window(self):
    import gtk
    self.outside_vbox.set_border_width(2)
    ok_button = gtk.Button("  Close  ")
    self.outside_vbox.pack_end(ok_button, False, False, 0)
    ok_button.connect("clicked", lambda b: self.destroy_window())
    self.window.connect("delete_event", lambda a, b: self.destroy_window())
    self.window.show_all()

  def destroy_window(self, *args):
    self.window.destroy()
    self.window = None

  def confirm_data(self, data):
    for data_key in self.data_keys :
      outlier_list = data.get(data_key)
      if outlier_list is not None and len(outlier_list) > 0 :
        return True
    return False

  def create_property_lists(self, data):
    import gtk
    for data_key in self.data_keys :
      outlier_list = data[data_key]
      if outlier_list is None or len(outlier_list) == 0 :
        continue
      else :
        frame = gtk.Frame(self.data_titles[data_key])
        vbox = gtk.VBox(False, 2)
        frame.set_border_width(6)
        frame.add(vbox)
        self.add_top_widgets(data_key, vbox)
        self.inside_vbox.pack_start(frame, False, False, 5)
        list_obj = residue_properties_list(
          columns=self.data_names[data_key],
          column_types=self.data_types[data_key],
          rows=outlier_list,
          box=vbox)

# Molprobity result viewer
class coot_molprobity_todo_list_gui(coot_extension_gui):
  data_keys = [ "rama", "rota", "cbeta", "probe" ]
  data_titles = { "rama"  : "Ramachandran outliers",
                  "rota"  : "Rotamer outliers",
                  "cbeta" : "C-beta outliers",
                  "probe" : "Severe clashes" }
  data_names = { "rama"  : ["Chain", "Residue", "Name", "Score"],
                 "rota"  : ["Chain", "Residue", "Name", "Score"],
                 "cbeta" : ["Chain", "Residue", "Name", "Conf.", "Deviation"],
                 "probe" : ["Atom 1", "Atom 2", "Overlap"] }
  if (gobject is not None):
    data_types = { "rama" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "rota" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "cbeta" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT],
                   "probe" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT] }
  else :
    data_types = dict([ (s, []) for s in ["rama","rota","cbeta","probe"] ])

  def __init__(self, data_file=None, data=None):
    assert ([data, data_file].count(None) == 1)
    if (data is None):
      data = load_pkl(data_file)
    if not self.confirm_data(data):
      return
    coot_extension_gui.__init__(self, "MolProbity to-do list")
    self.dots_btn = None
    self.dots2_btn = None
    self._overlaps_only = True
    self.window.set_default_size(420, 600)
    self.create_property_lists(data)
    self.finish_window()

  def add_top_widgets(self, data_key, box):
    import gtk
    if data_key == "probe" :
      hbox = gtk.HBox(False, 2)
      self.dots_btn = gtk.CheckButton("Show Probe dots")
      hbox.pack_start(self.dots_btn, False, False, 5)
      self.dots_btn.connect("toggled", self.toggle_probe_dots)
      self.dots2_btn = gtk.CheckButton("Overlaps only")
      hbox.pack_start(self.dots2_btn, False, False, 5)
      self.dots2_btn.connect("toggled", self.toggle_all_probe_dots)
      self.dots2_btn.set_active(True)
      self.toggle_probe_dots()
      box.pack_start(hbox, False, False, 0)

  def toggle_probe_dots(self, *args):
    if self.dots_btn is not None :
      show_dots = self.dots_btn.get_active()
      overlaps_only = self.dots2_btn.get_active()
      if show_dots :
        self.dots2_btn.set_sensitive(True)
      else :
        self.dots2_btn.set_sensitive(False)
      show_probe_dots(show_dots, overlaps_only)

  def toggle_all_probe_dots(self, *args):
    if self.dots2_btn is not None :
      self._overlaps_only = self.dots2_btn.get_active()
      self.toggle_probe_dots()

class rsc_todo_list_gui(coot_extension_gui):
  data_keys = ["by_res", "by_atom"]
  data_titles = ["Real-space correlation by residue",
                 "Real-space correlation by atom"]
  data_names = {}
  data_types = {}

class residue_properties_list(object):
  def __init__(self, columns, column_types, rows, box,
      default_size=(380,200)):
    assert len(columns) == (len(column_types) - 1)
    if (len(rows) > 0) and (len(rows[0]) != len(column_types)):
      raise RuntimeError("Wrong number of rows:\n%s" % str(rows[0]))
    import gtk
    self.liststore = gtk.ListStore(*column_types)
    self.listmodel = gtk.TreeModelSort(self.liststore)
    self.listctrl = gtk.TreeView(self.listmodel)
    self.listctrl.column = [None]*len(columns)
    self.listctrl.cell = [None]*len(columns)
    for i, column_label in enumerate(columns):
      cell = gtk.CellRendererText()
      column = gtk.TreeViewColumn(column_label)
      self.listctrl.append_column(column)
      column.set_sort_column_id(i)
      column.pack_start(cell, True)
      column.set_attributes(cell, text=i)
    self.listctrl.get_selection().set_mode(gtk.SELECTION_SINGLE)
    for row in rows :
      self.listmodel.get_model().append(row)
    self.listctrl.connect("cursor-changed", self.OnChange)
    sw = gtk.ScrolledWindow()
    w, h = default_size
    if len(rows) > 10 :
      sw.set_size_request(w, h)
    else :
      sw.set_size_request(w, 30 + (20 * len(rows)))
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    box.pack_start(sw, False, False, 5)
    inside_vbox = gtk.VBox(False, 0)
    sw.add(self.listctrl)

  def OnChange(self, treeview):
    import coot # import dependency
    selection = self.listctrl.get_selection()
    (model, tree_iter) = selection.get_selected()
    if tree_iter is not None :
      row = model[tree_iter]
      xyz = row[-1]
      if isinstance(xyz, tuple) and len(xyz) == 3 :
        set_rotation_centre(*xyz)
        set_zoom(30)
        graphics_draw()

def show_probe_dots(show_dots, overlaps_only):
  import coot # import dependency
  n_objects = number_of_generic_objects()
  sys.stdout.flush()
  if show_dots :
    for object_number in range(n_objects):
      obj_name = generic_object_name(object_number)
      if overlaps_only and not obj_name in ["small overlap", "bad overlap"] :
        sys.stdout.flush()
        set_display_generic_object(object_number, 0)
      else :
        set_display_generic_object(object_number, 1)
  else :
    sys.stdout.flush()
    for object_number in range(n_objects):
      set_display_generic_object(object_number, 0)

def load_pkl(file_name):
  pkl = open(file_name, "rb")
  data = pickle.load(pkl)
  pkl.close()
  return data

data = {}
data['rama'] = [('A', ' 535 ', 'PRO', 0.010273040428438598, (9.689999999999994, -50.069, 0.4069999999999999))]
data['omega'] = [('A', ' 535 ', 'PRO', None, (9.140999999999998, -49.881999999999984, 1.761))]
data['rota'] = [('A', ' 141 ', 'SER', 0.01071998049155809, (16.770999999999997, -4.479, -18.628)), ('A', ' 215 ', 'SER', 0.004246465154004574, (42.196, -13.681999999999999, -33.27)), ('A', ' 267 ', 'THR', 0.26534781697489723, (42.571, -22.724, -22.343)), ('A', ' 270 ', 'SER', 0.2795947426299252, (36.91699999999999, -23.245000000000005, -13.717)), ('A', ' 373 ', 'THR', 0.27610239704819156, (29.56399999999999, -42.48899999999998, -39.291999999999994)), ('A', ' 426 ', 'THR', 0.13674540422008327, (7.393999999999999, -30.156999999999993, -49.029)), ('A', ' 491 ', 'THR', 0.2713352131893119, (14.135000000000014, -57.108, -16.867)), ('A', ' 551 ', 'VAL', 0.010786726521610527, (3.938999999999999, -10.594999999999997, -25.793))]
data['cbeta'] = []
data['probe'] = [(' A 491  THR HG23', ' A 493  THR HG23', -0.748, (11.781, -54.807, -16.464)), (' A 426  THR HG22', ' A 431  TRP  HE1', -0.717, (8.241, -32.453, -47.271)), (' A 802  C8E  H13', ' A 802  C8E  H52', -0.697, (5.542, -37.881, -40.366)), (' A 347  GLN  NE2', ' A 645  HOH  O  ', -0.691, (30.487, -29.619, -48.008)), (' A 426  THR HG22', ' A 431  TRP  NE1', -0.605, (8.552, -32.454, -46.308)), (' A 123  ILE  O  ', ' A 417  GLN  NE2', -0.598, (24.044, -41.571, -27.868)), (' A 437  ARG HH21', ' A 460  ARG  HD2', -0.577, (16.667, -53.776, -28.716)), (' A 802  C8E  H11', ' A 802  C8E H172', -0.573, (4.581, -39.733, -37.687)), (' A 160  LEU HD22', ' A 166  VAL HG21', -0.562, (38.26, -2.726, -24.149)), (' A 293  MET  HE3', ' A 322  THR HG22', -0.559, (36.483, -32.66, -8.177)), (' A 516  TRP  CE3', ' A 551  VAL HG13', -0.559, (0.713, -11.561, -27.195)), (' A 160  LEU HD22', ' A 166  VAL  CG2', -0.559, (38.11, -3.391, -24.531)), (' A   7  THR  O  ', ' A  19  ARG  HG3', -0.555, (23.306, -23.768, -40.192)), (' A 800  C8E H131', ' A 805  C8E  H81', -0.518, (37.033, -50.516, -33.3)), (' A  56  GLN  HG3', ' A  64  SER  HB3', -0.505, (15.483, -28.725, -12.078)), (' A 373  THR HG22', ' A 374  SER  N  ', -0.487, (28.561, -41.749, -41.553)), (' A 348  VAL  O  ', ' A 348  VAL HG23', -0.474, (28.997, -38.615, -53.868)), (' A 422  PHE  CG ', ' A 801  C8E  H11', -0.471, (11.102, -40.511, -45.675)), (' A 496  LEU  O  ', ' A 497  ARG  HB2', -0.464, (13.154, -41.519, -14.61)), (' A 534  TYR  CD2', ' A 535  PRO  N  ', -0.46, (10.414, -50.172, 2.597)), (' A 436  TYR  CZ ', ' A 463  GLY  HA3', -0.459, (13.872, -42.604, -29.573)), (' A 347  GLN  HB3', ' A 624  HOH  O  ', -0.456, (27.372, -33.371, -51.489)), (' A 516  TRP  CZ3', ' A 551  VAL HG13', -0.454, (0.569, -11.119, -26.359)), (' A 150  GLN  NE2', ' A 152  TYR  OH ', -0.453, (13.995, -4.763, -7.682)), (' A 574  GLU  HG2', ' A 579  TYR  O  ', -0.446, (5.787, -31.461, -7.755)), (' A 175  THR  CG2', ' A 175  THR  O  ', -0.443, (13.176, -17.167, -6.594)), (' A 175  THR  O  ', ' A 175  THR HG23', -0.442, (12.92, -17.684, -6.431)), (' A 687  HOH  O  ', ' A 801  C8E  C19', -0.437, (5.446, -26.076, -58.749)), (' A 200  LYS  O  ', ' A 223  TYR  HA ', -0.432, (27.033, -14.404, -10.139)), (' A 242  THR HG22', ' A 243  ARG  N  ', -0.425, (21.849, -22.265, 1.266)), (' A 212  ASP  N  ', ' A 212  ASP  OD1', -0.424, (43.417, -10.523, -40.965)), (' A 160  LEU  CD2', ' A 166  VAL HG21', -0.424, (38.061, -2.346, -23.899)), (' A 293  MET  HE3', ' A 322  THR  CG2', -0.418, (36.344, -32.884, -8.187)), (' A 198  LEU  O  ', ' A 225  ASN  HA ', -0.414, (22.479, -17.213, -6.179)), (' A 491  THR HG23', ' A 493  THR  CG2', -0.414, (11.791, -54.442, -15.943)), (' A 803  C8E  C10', ' A 803  C8E H172', -0.413, (34.041, -43.541, -42.113)), (' A  44  ASP  HA ', ' A  47  ARG  HG2', -0.412, (12.028, -24.802, -19.957)), (' A 426  THR  CG2', ' A 431  TRP  HE1', -0.41, (7.717, -32.775, -46.871)), (' A  19  ARG  HB3', ' A  19  ARG  HE ', -0.408, (21.236, -27.573, -38.908)), (' A 527  TYR  CE1', ' A 540  LYS  HG3', -0.408, (2.658, -44.911, -15.38)), (' A 373  THR HG21', ' A 803  C8E H131', -0.408, (30.957, -44.276, -42.37)), (' A 687  HOH  O  ', ' A 801  C8E H192', -0.406, (5.293, -26.188, -58.667)), (' A 393  TYR  HA ', ' A 413  GLU  O  ', -0.403, (29.956, -45.251, -22.199)), (' A 168  LEU HD12', ' A 604  MTN  H41', -0.401, (32.026, -2.565, -19.57)), (' A 134  ASP  O  ', ' A 135  GLU  HG2', -0.401, (25.039, -8.811, -32.496)), (' A  38  GLN  NE2', ' A 562  ARG  HB3', -0.4, (7.973, -10.269, -22.929)), (' A 687  HOH  O  ', ' A 801  C8E H191', -0.4, (6.159, -25.57, -58.956))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)


import unittest
import tempfile
from pathlib import Path

from nucleo.motor import MotorFlujos
from persistencia.csv_manager import CSVManager
from persistencia.auditoria import Auditoria


class TestSistema(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.aud = Auditoria(Path(self.tmp.name) / "auditoria_log.csv")
        self.m = MotorFlujos(self.aud)
        self.m.agregar_usuario(1, "Admin", "123", "ADMIN", actor_id=0, registrar=False)
        self.m.agregar_usuario(2, "Ana", "abc", "USUARIO", actor_id=1)

    def tearDown(self):
        self.tmp.cleanup()

    def test_01_login(self):
        self.assertEqual(self.m.autenticar(2, "abc").nombre, "Ana")

    def test_02_login_invalido(self):
        with self.assertRaises(ValueError):
            self.m.autenticar(2, "mala")

    def test_03_rol_usuario_no_crea(self):
        with self.assertRaises(PermissionError):
            self.m.crear_tarea(10, "ALTA", 2, "X", actor_id=2)

    def test_04_admin_crea_tarea(self):
        self.m.crear_tarea(10, "ALTA", 2, "X", actor_id=1)
        self.assertIsNotNone(self.m.buscar_tarea(10))

    def test_05_id_tarea_duplicado(self):
        self.m.crear_tarea(10, "ALTA", 2, "X", actor_id=1)
        with self.assertRaises(ValueError):
            self.m.crear_tarea(10, "MEDIA", 2, "Y", actor_id=1)

    def test_06_usuario_solo_modifica_suya(self):
        self.m.agregar_usuario(3, "Luis", "x", "USUARIO", actor_id=1)
        self.m.crear_tarea(10, "MEDIA", 3, "X", actor_id=1)
        with self.assertRaises(PermissionError):
            self.m.cambiar_estado_tarea(10, "COMPLETADA", 2)

    def test_07_usuario_modifica_suya(self):
        self.m.crear_tarea(10, "MEDIA", 2, "X", actor_id=1)
        self.m.cambiar_estado_tarea(10, "COMPLETADA", 2)
        self.assertEqual(self.m.buscar_tarea(10).estado, "COMPLETADA")

    def test_08_prioridad_primero(self):
        self.m.crear_tarea(10, "MEDIA", 2, "Regular", actor_id=1)
        self.m.crear_tarea(11, "ALTA", 2, "Urgente", actor_id=1)
        self.assertEqual(self.m.ejecutar_siguiente(1).id_tarea, 11)

    def test_09_sla_escalamiento(self):
        self.m.crear_tarea(10, "MEDIA", 2, "Regular", actor_id=1)
        for i in range(3):
            self.m.crear_tarea(20+i, "ALTA", 2, f"Urgente{i}", actor_id=1)
            self.m.ejecutar_siguiente(1)
        t = self.m.buscar_tarea(10)
        self.assertEqual(t.prioridad, "ALTA")

    def test_10_auditoria_estado(self):
        self.m.crear_tarea(10, "MEDIA", 2, "X", actor_id=1)
        self.m.cambiar_estado_tarea(10, "COMPLETADA", 2)
        texto = (Path(self.tmp.name) / "auditoria_log.csv").read_text(encoding="utf-8")
        self.assertIn("CAMBIO_ESTADO", texto)

    def test_11_undo_redo(self):
        self.m.crear_tarea(10, "MEDIA", 2, "X", actor_id=1)
        self.m.deshacer(1)
        self.assertIsNone(self.m.buscar_tarea(10))
        self.m.rehacer(1)
        self.assertIsNotNone(self.m.buscar_tarea(10))

    def test_12_persistencia(self):
        self.m.crear_tarea(10, "MEDIA", 2, "Persistir", actor_id=1)
        gestor = CSVManager(Path(self.tmp.name) / "data")
        gestor.guardar_todo(self.m)

        m2 = MotorFlujos(self.aud)
        gestor.cargar_todo(m2)
        self.assertIsNotNone(m2.usuarios.buscar(2))
        self.assertIsNotNone(m2.buscar_tarea(10))


if __name__ == "__main__":
    unittest.main()

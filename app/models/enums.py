# app/models/enums.py

from enum import Enum


class UniandesMajor(str, Enum):
    """Carreras de pregrado de la Universidad de los Andes."""
    INGENIERIA_SISTEMAS     = "Ingeniería de Sistemas y Computación"
    INGENIERIA_CIVIL        = "Ingeniería Civil"
    INGENIERIA_ELECTRICA    = "Ingeniería Eléctrica y Electrónica"
    INGENIERIA_MECANICA     = "Ingeniería Mecánica"
    INGENIERIA_BIOMEDICA    = "Ingeniería Biomédica"
    INGENIERIA_AMBIENTAL    = "Ingeniería Ambiental"
    INGENIERIA_QUIMICA      = "Ingeniería Química"
    INGENIERIA_INDUSTRIAL   = "Ingeniería Industrial"
    MATEMATICAS             = "Matemáticas"
    FISICA                  = "Física"
    QUIMICA                 = "Química"
    BIOLOGIA                = "Biología"
    MICROBIO_BIOINFORMATICA = "Microbiología y Bioinformática"
    MEDICINA                = "Medicina"
    PSICOLOGIA              = "Psicología"
    DERECHO                 = "Derecho"
    ADMINISTRACION          = "Administración de Empresas"
    ECONOMIA                = "Economía"
    FINANZAS                = "Finanzas y Contaduría Pública"
    ARQUITECTURA            = "Arquitectura"
    DISEÑO                  = "Diseño"
    ARTE                    = "Arte"
    MUSICA                  = "Música"
    FILOSOFIA               = "Filosofía"
    HISTORIA                = "Historia"
    LITERATURA              = "Literatura"
    LENGUAS                 = "Lenguas y Cultura"
    CIENCIA_POLITICA        = "Ciencia Política"
    ANTROPOLOGIA            = "Antropología"
    PERIODISMO              = "Periodismo y Opinión Pública"
    COMUNICACION            = "Comunicación Social"
    OTRO                    = "Otro"
    
class SessionStatus(str, Enum):
    PENDIENTE   = "Pendiente"
    CANCELADA   = "Cancelada"
    CONCLUIDA   = "Concluida"
    EN_REVISION = "En Revisión"


class PQRType(str, Enum):
    QUEJA    = "Queja"
    RECLAMO  = "Reclamo"
    PETICION = "Petición"
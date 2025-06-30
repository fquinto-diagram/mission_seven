from app.libraries.number_formatter import NumberFormatter

class Calculator:
    
    #TODO: refact methods when make invoices

   def calculate_discounts(uni, pre, dto1, dto2, dto3, dto, dtoac, dtopp, deci_base):
    base = round(uni * pre, deci_base)
    base = round(base - (base * dto1 / 100), deci_base)
    base = round(base - (base * dto2 / 100), deci_base)
    base = round(base - (base * dto3 / 100), deci_base)

    impdto1 = round(base * dto / 100, deci_base)
    base = round(base - impdto1, deci_base)
    impdto2 = round(base * dtoac / 100, deci_base)
    base = round(base - impdto2, deci_base)
    impdto3 = round(base * dtopp / 100, deci_base)
    base = round(base - impdto3, deci_base)
    return base


def calcula_factura_vta(contenedor, lineas, irpf, tirpf):
    tbase = tciva = tcrec = 0
    for uni, pre, dto, dtoac, dtopp, dto1, dto2, iva, rec in lineas:
        deci_base = contenedor.facturaventa.campo("C016").decimales
        uni = round(uni, contenedor.facturaventalin.campo("C005").decimales)
        pre = round(pre, contenedor.facturaventalin.campo("C006").decimales)
        base = Calculator.calculate_discounts(uni, pre, dto1, dto2, 0, dto, dtoac, dtopp, deci_base)
        tciva += round(base * iva / 100, contenedor.facturaventa.campo("C017").decimales)
        tcrec += round(base * rec / 100, contenedor.facturaventa.campo("C018").decimales)
        tbase += base

    cirpf = tbase * irpf / 100 if tirpf == "B" else (tbase + tciva + tcrec) * irpf / 100
    cirpf = round(cirpf, contenedor.facturaventalin.campo("C009").decimales)
    total = tbase + tciva + tcrec - cirpf

    return {
        "#id_base_imponible": tbase,
        "#id_cuota_iva": tciva,
        "#id_cuota_recargo": tcrec,
        "#id_porcentaje_irpf": irpf,
        "#id_cuota_irpf": cirpf,
        "#id_total": total,
    }


def calcula_factura_com(contenedor, lineas, irpf, tirpf, exentairpf):
    tbase0 = tbase= tciva = tcrec = 0
    for uni, pre, dto, dtoac, dtopp, dto1, dto2, dto3, iva, rec in lineas:
        deci_base = contenedor.facturacompra.campo("C021").decimales
        base = Calculator.calculate_discounts(uni, pre, dto1, dto2, dto3, dto, dtoac, dtopp, deci_base)
        tciva += round(base * iva / 100, contenedor.facturacompra.campo("C022").decimales)
        tcrec += round(base * rec / 100, contenedor.facturacompra.campo("C023").decimales)
        if iva == 0:
            tbase0 += base
        else:
            tbase += base

    baseirfp = tbase if exentairpf == "N" else tbase0 + tbase
    cirpf = baseirfp * irpf / 100 if tirpf == "B" else (baseirfp + tciva + tcrec) * irpf / 100

    cirpf = round(cirpf, contenedor.facturacompra.campo("C031").decimales)
    total = tbase0 + tbase + tciva + tcrec - cirpf

    return {
        "#id_base_imponible": tbase + tbase0,
        "#id_cuota_iva": tciva,
        "#id_cuota_recargo": tcrec,
        "#id_porcentaje_irpf": irpf,
        "#id_cuota_irpf": cirpf,
        "#id_total": total,
    }


def calcula_presupuesto_vta(contenedor, lineas, irpf, tirpf):
    tbase = tciva = tcrec = 0
    for uni, pre, dto, dtoac, dtopp, dto1, dto2, iva, rec in lineas:
        deci_base = contenedor.presupuesto.campo("C016").decimales
        base = Calculator.calculate_discounts(uni, pre, dto1, dto2, 0, dto, dtoac, dtopp, deci_base)
        tciva += round(base * iva / 100, contenedor.presupuesto.campo("C017").decimales)
        tcrec += round(base * rec / 100, contenedor.presupuesto.campo("C018").decimales)
        tbase += base

    cirpf = tbase * irpf / 100 if tirpf == "B" else (tbase + tciva + tcrec) * irpf / 100
    cirpf = round(cirpf, contenedor.presupuesto.campo("C041").decimales)
    total = tbase + tciva + tcrec - cirpf

    return {
        "#id_base_imponible": tbase,
        "#id_cuota_iva": tciva,
        "#id_cuota_recargo": tcrec,
        "#id_porcentaje_irpf": irpf,
        "#id_cuota_irpf": cirpf,
        "#id_total": total,
    }


def calcula_pedido_vta(contenedor, lineas):
    tbase = tservi = 0
    for uni, servi, pre, dto, dtoac, dtopp, dto1, dto2, iva, rec in lineas:
        deci_base = contenedor.pedidoventa.campo("C011").decimales
        uni = round(uni, contenedor.pedidoventalin.campo("C005").decimales)
        servi = round(servi, contenedor.pedidoventalin.campo("C005").decimales)
        pre = round(pre, contenedor.pedidoventalin.campo("C006").decimales)
        base = Calculator.calculate_discounts(uni, pre, dto1, dto2, 0, dto, dtoac, dtopp, deci_base)
        base_servi = Calculator.calculate_discounts(servi, pre, dto1, dto2, 0, dto, dtoac, dtopp, deci_base)
        tbase += base
        tservi += base_servi

    tpdte = tbase - tservi

    return {
        "#id_pservir": tpdte,
        "#id_servido": tservi,
        "#id_total": tbase,
    }


def calcula_albaran_vta(contenedor, lineas, irpf, tirpf):
    tbase = tciva = tcrec = 0
    for uni, pre, dto, dtoac, dtopp, dto1, dto2, iva, rec in lineas:
        deci_base = contenedor.albaranventa.campo("C016").decimales
        uni = round(uni, contenedor.albaranventalin.campo("C005").decimales)
        pre = round(pre, contenedor.albaranventalin.campo("C006").decimales)
        base = Calculator.calculate_discounts(uni, pre, dto1, dto2, 0, dto, dtoac, dtopp, deci_base)
        tciva += round(base * iva / 100, contenedor.albaranventa.campo("C017").decimales)
        tcrec += round(base * rec / 100, contenedor.albaranventa.campo("C018").decimales)
        tbase += base

    cirpf = tbase * irpf / 100 if tirpf == "B" else (tbase + tciva + tcrec) * irpf / 100
    cirpf = round(cirpf, contenedor.facturaventalin.campo("C009").decimales)
    total = tbase + tciva + tcrec - cirpf

    return {
        "#id_base_imponible": tbase,
        "#id_cuota_iva": tciva,
        "#id_cuota_recargo": tcrec,
        "#id_porcentaje_irpf": irpf,
        "#id_cuota_irpf": cirpf,
        "#id_total": total,
    }


def calcula_factura_vta2(contenedor, lineas, irpf, tirpf):
    tbase = tciva = tcrec = 0
    for base, iva, rec in lineas:
        tbase += base
        tciva += iva
        tcrec += rec

    cirpf = tbase * irpf / 100 if tirpf == "B" else (tbase + tciva + tcrec) * irpf / 100
    cirpf = round(cirpf, contenedor.facturaventalin.campo("C009").decimales)
    total = tbase + tciva + tcrec - cirpf

    return {
        "#id_base_imponible": tbase,
        "#id_cuota_iva": tciva,
        "#id_cuota_recargo": tcrec,
        "#id_porcentaje_irpf": irpf,
        "#id_cuota_irpf": cirpf,
        "#id_total": total,
    }


def calcula_pedido_com(contenedor, lineas):
    tbase = treci = 0
    for uni, reci, pre, dto, dtoac, dtopp, dto1, dto2, dto3, iva, rec in lineas:
        deci_base = contenedor.pedidoventa.campo("C011").decimales
        uni = round(uni, contenedor.pedidoventalin.campo("C005").decimales)
        reci = round(reci, contenedor.pedidoventalin.campo("C005").decimales)
        pre = round(pre, contenedor.pedidoventalin.campo("C006").decimales)
        base = Calculator.calculate_discounts(uni, pre, dto1, dto2, dto3, dto, dtoac, dtopp, deci_base)
        base_reci = Calculator.calculate_discounts(reci, pre, dto1, dto2, dto3, dto, dtoac, dtopp, deci_base)
        tbase += base
        treci += base_reci

    tpdte = tbase - treci

    return {
        "#id_precibir": tpdte,
        "#id_recibido": treci,
        "#id_total": tbase,
    }


def calcula_albaran_com(contenedor, lineas, irpf, tirpf):
    tbase = tciva = tcrec = 0
    for uni, pre, dto, dtoac, dtopp, dto1, dto2, dto3, iva, rec in lineas:
        deci_base = contenedor.albarancompra.campo("C016").decimales
        uni = round(uni, contenedor.albarancompralin.campo("C005").decimales)
        pre = round(pre, contenedor.albarancompralin.campo("C006").decimales)
        base = Calculator.calculate_discounts(uni, pre, dto1, dto2, dto3, dto, dtoac, dtopp, deci_base)
        tciva += round(base * iva / 100, contenedor.albarancompra.campo("C017").decimales)
        tcrec += round(base * rec / 100, contenedor.albarancompra.campo("C018").decimales)
        tbase += base

    cirpf = tbase * irpf / 100 if tirpf == "B" else (tbase + tciva + tcrec) * irpf / 100
    cirpf = round(cirpf, contenedor.facturaventalin.campo("C009").decimales)
    total = tbase + tciva + tcrec - cirpf

    return {
        "#id_base_imponible": tbase,
        "#id_cuota_iva": tciva,
        "#id_cuota_recargo": tcrec,
        "#id_porcentaje_irpf": irpf,
        "#id_cuota_irpf": cirpf,
        "#id_total": total,
    }


def calcula_factura_com2(contenedor, lineas, irpf, tirpf, exentairpf):
    tbase = tciva = tcrec = 0
    for base, iva, rec in lineas:
        tbase += base
        tciva += iva
        tcrec += rec

    if exentairpf:
        cirpf = tbase * irpf / 100 if tirpf == "B" else tbase * irpf / 100
    else:
        cirpf = tbase * irpf / 100 if tirpf == "B" else (tbase + tciva + tcrec) * irpf / 100

    cirpf = round(cirpf, contenedor.facturacompra.campo("C031").decimales)
    total = tbase + tciva + tcrec - cirpf

    return {
        "#id_base_imponible": tbase,
        "#id_cuota_iva": tciva,
        "#id_cuota_recargo": tcrec,
        "#id_porcentaje_irpf": irpf,
        "#id_cuota_irpf": cirpf,
        "#id_total": total,
    }

    
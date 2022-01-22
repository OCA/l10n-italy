#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
import typing

from odoo.exceptions import UserError


def same_payment_method(account_move_lines):
    '''Ensures all lines have the same payment method'''
    
    assert len(account_move_lines) > 0
    
    pay_method = None
    
    for line in account_move_lines:
        
        line_pay_method = line.payment_method
        
        if pay_method is None:
            pay_method = line_pay_method
            
        elif line_pay_method.id != pay_method.id:
            raise UserError(
                'Le scadenze selezionate devono avere '
                'tutte lo stesso metodo di pagamento'
            )
        
        else:
            pass
        
        # end if
        
    # end for
    
    return pay_method
    


def allowed_payment_method(account_move_lines, payment_method_codes: typing.List[str]):
    '''Ensures the selected lines have a supported payment method'''
    
    assert len(account_move_lines) > 0
    
    assert len(payment_method_codes) > 0, \
        'At least one payment method code must be specified ' \
        '...otherwise what are you calling this function for????'
    
    for line in account_move_lines:
        
        if line.payment_method.code not in payment_method_codes:
            raise UserError(
                'La funzione è supportata solo '
                'per i seguenti metodi di pagamento:'
                ' ' + ', '.join(payment_method_codes)
            )
        # end if
        
    # end for
    


def assigned_to_payment_order(account_move_lines, assigned: bool):
    '''
    Check if the selected lines are assigned to a payment order or not.
    If the "assigned" parameters is:
    
      - True the method requires that all lines have been assigned to a
        payment order, raises an exception otherwise
    
      - False the method requires that all lines have NOT been assigned to a
        payment order, raises an exception otherwise
    '''
    
    assert len(account_move_lines) > 0
    
    for line in account_move_lines:

        if assigned and not line.in_order:
            raise UserError(
                'Le scadenze selezionate devono essere '
                'assegnate ad un ordine di pagamento'
            )
        elif not assigned and line.in_order:
            raise UserError(
                'Le scadenze selezionate non possono essere '
                'già assegnate ad un ordine di pagamento'
            )
        else:
            pass
        # end if
        
    # end for
    


def same_payment_order(account_move_lines):
    '''Ensures that all the move lines are in the same payment_order'''
    
    assert len(account_move_lines) > 0
    
    po_name = account_move_lines[0].payment_order_name
    
    for line in account_move_lines:
        
        if line.payment_order_name != po_name:
            raise UserError(
                'Per poter procedere con l\'operazione tutte le righe '
                'selezionate devono appartenere allo stesso ordine di '
                'pagamento'
            )
        else:
            pass
        
        # end if
        
    # end for

    return po_name
    


def allowed_payment_order_status(account_move_lines, payment_order_status: typing.List[str]):
    '''
    Ensures that all the payment orders referenced by the lines are in one of
    the valid statuses listed in the payment_order_status parameter
    '''
    
    assert len(account_move_lines) > 0
    
    assert len(payment_order_status) > 0, \
        'At least one state must be specified ' \
        '...otherwise what are you calling this function for????'
    
    for line in account_move_lines:

        if line.state not in payment_order_status:
            
            # Translate the values to user friendly labels
            val_to_label = dict(line.fields_get(['state'])['state']['selection'])
            labels_list = [val_to_label[x] for x in payment_order_status]
            
            if len(payment_order_status) > 1:
                msg = 'in uno dei seguenti stati: ' + ', '.join(labels_list)
            else:
                msg = 'nello stato: ' + labels_list[0]
            # end if
            
            raise UserError(
                'Per poter procedere con l\'operazione l\'ordine di pagamento '
                'di ciascuna scadenza selezionata deve essere ' + msg
            )
        # end if
        
    # end for
    


def except_payment_order_status(account_move_lines,
                                payment_order_status: typing.List):
    '''
    Ensures that all the payment orders referenced by the lines are not in
    one of the valid statuses listed in the payment_order_status parameter
    '''

    for line in account_move_lines:

        if line.state in payment_order_status:
            raise UserError(
                'Per poter procedere con l\'operazione l\'ordine '
                'di pagamento di ciascuna scadenza selezionata non deve '
                'essere nello stato "Documento Caricato"'
            )
        # end if

    # end for



def lines_has_payment(account_move_lines, paid: bool):
    """
    Check if the selected lines are paid or not.
    If the "paid" parameters is:

      - True check against incasso_effettuato must be the same,
        raises an exception otherwise

      - False check against incasso_effettuato must be the same,
        raises an exception otherwise
    """

    assert len(account_move_lines) > 0

    for line in account_move_lines:

        if paid and not line.incasso_effettuato:
            raise UserError(
                'Le scadenze selezionate devono avere '
                'l\'incasso effettuato'
            )
        elif not paid and line.incasso_effettuato:
            raise UserError(
                'Le scadenze selezionate non devono avere '
                'l\'incasso effettuato'
            )
        else:
            pass
        # end if

    # end for



def lines_check_invoice_type(account_move_lines,
                             allowed_documents: typing.List[str]):
    """
    Check if the selected lines document type is in the list.
    """

    assert len(account_move_lines) > 0

    documents_allowed = []

    document_labels = {
        'out_invoice': 'Fattura attiva',
        'in_invoice': 'Fattura passiva',
        'out_refund': 'Nota di credito cliente',
        'in_refund': 'Nota di credito fornitore',
    }

    for inv_type in allowed_documents:
        documents_allowed.append(document_labels[inv_type])
    # end for

    for line in account_move_lines:

        if line.invoice_id.type not in allowed_documents:
            raise UserError(
                'La funzione è supportata solo '
                'per i tipi di documento: '
                ' ' + ', '.join(documents_allowed)
            )
        # end if

    # end for



def insoluto(account_move_lines):
    same_payment_method(account_move_lines)
    assigned_to_payment_order(account_move_lines, assigned=True)
    same_payment_order(account_move_lines)
    allowed_payment_order_status(account_move_lines, ['done'])
    lines_has_payment(account_move_lines, paid=True)
    lines_check_invoice_type(account_move_lines, ['out_invoice'])


def payment_confirm(account_move_lines):

    # incasso effettuato deve essere False
    lines_has_payment(account_move_lines, paid=False)

    same_payment_method(account_move_lines)
    allowed_payment_method(
        account_move_lines,
        ['invoice_financing', 'riba_cbi', 'sepa_direct_debit'],
    )
    assigned_to_payment_order(account_move_lines, assigned=True)
    allowed_payment_order_status(account_move_lines, ['done'])
    same_payment_order(account_move_lines)
    lines_check_invoice_type(account_move_lines, ['out_invoice'])

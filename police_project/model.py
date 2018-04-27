# -*- coding: utf-8 -*-
import datetime
from datetime import timedelta
from openerp import models, fields, api, http

class PoliceDetail(models.Model):
    _name = 'police.detail'
    _rec_name = 'number'
    number = fields.Char(string="Report Number")
    case_id = fields.Char(string="Case ID",required=False,)
    date = fields.Date(default = datetime.date.today())
    day = fields.Char()
    time = fields.Char(required=True)
    road_name = fields.Many2one('road.name', string="Road Name",required=True,)
    center_name = fields.Many2one('center.name', string="Center Name",required=True,)
    location_name = fields.Char(string="Location Name",required=True,)
    digital_tag = fields.Many2one('digital.tag', string="Digital Tag",required=True,)
    direction_name = fields.Many2one('direction.name', string="Direction Name",required=True,)
    violation = fields.Char(string='Time of Case', required=True, placeholder="ساعة")
    violation_1 = fields.Char(string=' ', required=True, placeholder="اللحظة")
    code = fields.Many2one(comodel_name="car.code",string='Code of Police CAR',required=True,)
    police_officer = fields.Char(string='Police Officer 1',required=True,)
    rank_officer = fields.Many2one('rank.of1',string='Rank of officer 1',required=True,)
    PID1 = fields.Char(string="Officer 1 ID",required=True, )
    PID2 = fields.Char(string="Officer 2 ID", required=False, )
    sex_of1 = fields.Selection(string="Gender", selection=[('m', 'ذكر'), ('f', 'أنثى'), ], required=True, )
    sex_of2 = fields.Selection(string="Gender", selection=[('m', 'ذكر'), ('f', 'أنثى'), ], required=False, )
    name_officer_2 = fields.Char(string='Police officer 2')
    rank_officer_2 = fields.Many2one('rank.of2',string='Rank of officer 2')
    tosc = fields.Char(string="Case submitting Time", required=True, placeholder="ساعة" )
    tosc_1 = fields.Char(string=" ", required=True, placeholder="اللحظة" )
    am_pm = fields.Selection(string=" ", selection=[('am', 'AM'), ('pm', 'PM'), ], required=True, )
    am_pm_1 = fields.Selection(string=" ", selection=[('am', 'AM'), ('pm', 'PM'), ], required=True, )
    receiving_party = fields.Many2one('receiving.party', string="Receiving Party",required=True,)
    receiving_party_rank = fields.Many2one('receiving.party.rank', string="Receiving Party Rank",required=True,)
    receiving_name = fields.Char(string="Receiving Party Name",required=True, )
    case_detail = fields.Text(string='Case details ')
    party_link = fields.One2many('party.detail', "main_class", string="Party Detail")
    case_type = fields.One2many('case.type', "main_class", string="Case Type")
    check_field = fields.Boolean(string="Check Fields",)
    check_tree = fields.Boolean(string="Check Tree",)
    preview = fields.Html('Report Preview',compute="generate_preview")

    def _check_PID1(self):
        for val in self.read(['PID1']):
            if val['PID1']:
                if len(val['PID1']) > 10:
                    return False
        return True

    def _check_PID2(self):
        for val in self.read(['PID2']):
            if val['PID2']:
                if len(val['PID2']) > 10:
                    return False
        return True
    _constraints = [
        (_check_PID1, 'should be less than 10 characters رقم الهوية .', ['PID1']),
        (_check_PID2, 'should be less than 10 characters رقم الهوية .', ['PID2'])
    ]

    @api.onchange('road_name','center_name','location_name','digital_tag',
                  'direction_name','violation','code','police_officer',
                  'rank_officer','PID1','sex_of1','tosc','receiving_party',
                  'receiving_party_rank','receiving_name')
    def _onchange_check_filed(self):
        if self.road_name and self.center_name and self.location_name and self.digital_tag and self.direction_name and \
                self.violation and self.code and self.police_officer and self.rank_officer and self.PID1 and self.sex_of1\
                and self.tosc and self.receiving_party and self.receiving_party_rank and self.receiving_name:
            self.check_field = True
        else:
            self.check_field = False

    @api.onchange('case_type')
    def onchange_method(self):
        if self.case_type:
            self.check_tree =True
        else:
            self.check_tree =False

    @api.one
    def generate_preview(self):
        self.preview = self.env['report'].get_html(self, 'police_case_summary.module_report')

    @api.multi
    def open_menu(self):
        return {'name': 'Police Record', 'domain': [], 'res_model': 'police.detail',
                'type': 'ir.actions.act_window', 'view_mode': 'form', 'view_type': 'form',
                'context': {}, 'target': 'self', }

    @api.model
    def create(self, val):
        val['number'] = self.env['ir.sequence'].next_by_code('rec.number')
        val['case_id'] = self.env['ir.sequence'].next_by_code('rec.case')
        new_record = super(PoliceDetail, self).create(val)
        return new_record

    def create_model_color(self):
        record = self.env['model.color'].create({
            'name':"Colors and Models"
        })

    def create_id_type(self):
        record1 = self.env['id.config'].create({
            'name':"ID What Found and Other Configurations"
        })

    def create_rank(self):
        record1 = self.env['rank.config'].create({
            'name':"Ranks Configuration"
        })

    @api.onchange('date')
    def _change_daytime(self):
        if self.date:
            self.day = datetime.datetime.strptime(self.date,'%Y-%m-%d').strftime('%A')
            self.time = (datetime.datetime.now() + timedelta(hours=5)).strftime("%I:%M:%S %p")
            # self.violation = (datetime.datetime.now() + timedelta(hours=5)).strftime("%I:%M:%S %p")
            # self.tosc = (datetime.datetime.now() + timedelta(hours=5)).strftime("%I:%M:%S %p")

    # def give_time(self):
    #     self.violation = (datetime.datetime.now() + timedelta(hours=5)).strftime("%I:%M:%S %p")
    #
    # def give_time1(self):
    #     self.tosc = (datetime.datetime.now() + timedelta(hours=5)).strftime("%I:%M:%S %p")

    # @api.onchange('violation')
    # def onchange_violation(self):
    #     self.violation = (datetime.datetime.now() + timedelta(hours=5)).strftime("%I:%M:%S %p")

class CaseType1(models.Model):
    _name = 'case.type1'
    _rec_name = 'case_type'
    case_type = fields.Many2one(comodel_name="type.case", string="Violation Type",required=True,)
    cate_case = fields.Many2one(comodel_name="cate.case", string="Violation Category", required=False, )
    qty = fields.Char(string="Quantity",  required=False, )
    vio_code = fields.Char(string="Violation Code ",  required=False, )
    vio_number = fields.Char(string="Violation Number",  required=False, )

    main_class = fields.Many2one(comodel_name="violation.detail", string="Violation Type", required=False, )


class CaseType(models.Model):
    _name = 'case.type'
    _rec_name = 'case_type'
    main_case = fields.Many2one(comodel_name="main.case", string="Case",required=True,)
    case_type = fields.Many2one(comodel_name="type.case", string="Case Type",required=False, )
    cate_case = fields.Many2one(comodel_name="cate.case", string="Detail",required=False, )
    sub_cate_case = fields.Many2one(comodel_name="case.sub.cate", string="More Detail", required=False, )
    abc = fields.Boolean(string="",  )
    xyz = fields.Boolean(string="",  )
    test = fields.Boolean(string="",  )

    @api.onchange('main_case')
    def onchange_main_case(self):
        if self.main_case:
            rec = self.env['type.case'].search([('id','=',self.main_case.id)])
            if rec:
                self.abc = True
            else:
                self.abc = False
                self.case_type = False

    @api.onchange('case_type')
    def onchange_case_type(self):
        if self.case_type:
            rec = self.env['cate.case'].search([('id', '=', self.case_type.id)])
            if rec:
                self.xyz = True
            else:
                self.cate_case = False
                self.xyz = False
    @api.onchange('cate_case')
    def onchange_cate_case(self):
        if self.cate_case:
            rec = self.env['case.sub.cate'].search([('id', '=', self.cate_case.id)])
            if rec:
                self.test = True
            else:
                self.test = False
                self.sub_cate_case = False


    main_class = fields.Many2one(comodel_name="police.detail", string="Case Type", required=False, )
    companion_class = fields.Many2one('companion.detail')

class HajjUmrah(models.Model):
    _name = 'hajj.umrah'
    _rec_name = 'case_id'

    # number = fields.Char(string="Report Number")
    case_id = fields.Char(string="Case ID",required=False,)
    date = fields.Date(default=datetime.date.today())
    day = fields.Char()
    time = fields.Char(required=True)
    road_name = fields.Many2one('road.name', string="Road Name",required=True,)
    center_name = fields.Many2one('center.name', string="Center Name",required=True,)

    violation_type = fields.One2many(comodel_name="hajjumrah.violation", inverse_name="main_class", string="Violation Information", required=False, )

    @api.model
    def create(self, vals):
        vals['case_id'] = self.env['ir.sequence'].next_by_code('rec.umrah')
        new_record = super(HajjUmrah, self).create(vals)
        return new_record


    @api.onchange('date')
    def _change_daytime(self):
        if self.date:
            self.day = datetime.datetime.strptime(self.date, '%Y-%m-%d').strftime('%A')
            self.time = (datetime.datetime.now() + timedelta(hours=5)).strftime("%I:%M:%S %p")


class HajjUmrahViolation(models.Model):
    _name = 'hajjumrah.violation'
    _rec_name = 'violation'

    violation = fields.Char(string="Violation name", required=False, )
    violation_type = fields.Char(string="Violation type", required=False, )
    nop = fields.Integer(string="Number of people", required=False, )
    remarks = fields.Text(string="Remarks", required=False, )

    main_class  = new_field_id = fields.Many2one(comodel_name="hajj.umrah", string="Hajj and Umrah", required=False, )


class PartyDetail(models.Model):
    _name = 'party.detail'

    name = fields.Char("Driver Name",required=True,)
    car_name = fields.Many2one(comodel_name="car.name",   string="Name of Car",required=False,)
    car_color = fields.Many2one(comodel_name="car.color", string="Color of Car",required=False,)
    car_model = fields.Many2one(comodel_name="car.model", string="Model of Car",required=False,)
    car_maker = fields.Many2one(comodel_name="car.maker", string="Maker of Car",required=False,)
    car_plate = fields.Char("Plate Number",required=False,)
    driver_country = fields.Many2one('res.country', "Nationality",required=True,)
    id_num = fields.Char("ID number",required=True,)
    sex = fields.Selection(string="Gender", selection=[('m', 'ذكر'), ('f', 'أنثى'), ],required=True,)
    id_type = fields.Many2one('id.type', "ID Type",required=True,)
    what_found = fields.Many2one('type.case', "What we found",required=False,)
    qty_uom = fields.Selection(string="Unit of Measure", selection=[('g', 'Grams'), ('k', 'Kgs'), ('p', 'Pieces'), ], required=False, )
    qty = fields.Integer(string="Quantity",required=False,)
    accident_reason = fields.Many2one('accident.reason',"Reason of accident ",required=False,)
    result = fields.Many2one('accident.result',"Results",required=False,)
    mean_trans = fields.Many2one('mean.trans', "Means of Transportation",required=False,)
    hospital_name = fields.Many2one('hospital.name', "Name of Hospital",required=False,)
    main_class = fields.Many2one('police.detail', "Party Detail",required=False,)
    remark = fields.Text("Remarks",required=False,)
    additional = fields.Text("Additional Details",required=False,)
    previous_record = fields.Boolean("Previous Records")
    companion_detail = fields.Boolean("Companion Details")

    previous_record_link = fields.One2many('previous.record', "main_class", string="Previous Record")
    companion_detail_link = fields.One2many('companion.detail', "main_class", string="Companion Detail")


class CompanionDetail(models.Model):
    _name = 'companion.detail'

    name = fields.Char("Name",required=True,)
    country = fields.Many2one('res.country', "Nationality",required=True,)
    id_num = fields.Char("ID number",required=True,)
    id_type = fields.Many2one('id.type', "ID Type",required=True,)
    relation = fields.Many2one('accident.relation',"Relation",required=False,)
    sex = fields.Selection(string="Gender", selection=[('m', 'ذكر'), ('f', 'أنثى'), ],required=True,)
    what_found = fields.Many2one('type.case',"What we found",required=False,)
    qty_uom = fields.Selection(string="Unit of Measure", selection=[('g', 'Grams'), ('k', 'Kgs'), ('p', 'Pieces'), ], required=False, )
    qty = fields.Integer(string="Qty",required=False, )
    accident_reason = fields.Many2one('accident.reason',"Reason of accident ",required=False,)
    result = fields.Many2one('accident.result',"Results",required=False,)
    mean_trans = fields.Many2one('mean.trans', "Means of Transportation",required=False,)
    hospital_name = fields.Many2one('hospital.name', "Name of Hospital",required=False,)
    previous_record = fields.Boolean("Previous Records")
    case_detail = fields.Boolean("Case Details")

    main_class = fields.Many2one('party.detail')
    previous_record_link = fields.One2many('previous.record', "companion_class", string="Previous Record")
    case_type_link = fields.One2many('case.type', "companion_class", string="Case Type")

class PreviousRecord(models.Model):
    _name = 'previous.record'

    ministry_name = fields.Many2one('ministry.name', "Name of Ministry",required=True,)
    no_complaint = fields.Char("Number Of Complaint",required=True,)
    date = fields.Date(required=True,)
    day = fields.Char(required=True,)

    main_class = fields.Many2one('party.detail')
    companion_class = fields.Many2one('companion.detail')

    @api.onchange('date')
    def _change_daytime(self):
        if self.date:
            self.day = datetime.datetime.strptime(self.date,'%Y-%m-%d').strftime('%A')
            self.time = (datetime.datetime.now() + timedelta(hours=5)).strftime("%I:%M:%S %p")


class ViolationDetail(models.Model):
    _name = 'violation.detail'
    _rec_name = 'number'

    number = fields.Char(string="Report Number")
    case_id = fields.Char(string="Case ID",required=False,)
    date = fields.Date(default=datetime.date.today())
    day = fields.Char()
    time = fields.Char(required=False)
    road_name = fields.Many2one('road.name', string="Road Name",required=False,)
    center_name = fields.Many2one('center.name', string="Center Name",required=False,)
    location_name = fields.Char( string="Location Name",required=False,)
    digital_tag = fields.Many2one('digital.tag', string="Digital Tag",required=False,)
    direction_name = fields.Many2one('direction.name', string="Direction Name",required=False,)
    violation = fields.Char(string='Time of Violation',required=False, placeholder="ساعة")
    violation_1 = fields.Char(string=' ',required=False, placeholder="اللحظة" )
    am_pm = fields.Selection(string=" ", selection=[('am', 'AM'), ('pm', 'PM'), ], required=False, )
    code = fields.Many2one(comodel_name="car.code",string='Code of Police CAR',required=False,)
    police_officer = fields.Char(string='Police Officer 1',required=False,)
    rank_officer = fields.Many2one('rank.of1',string='Rank of officer 1',required=False,)
    PID1 = fields.Char(string="Officer 1 ID",required=False,)
    sex_of1 = fields.Selection(string="Gender", selection=[('m', 'ذكر'), ('f', 'أنثى'), ],required=False, )
    sex_of2 = fields.Selection(string="Gender", selection=[('m', 'ذكر'), ('f', 'أنثى'), ],required=False, )
    name_officer_2 = fields.Char(string='Police officer 2')
    rank_officer_2 = fields.Many2one('rank.of2',string='Rank of officer 2')
    PID2 = fields.Char(string="Officer 2 ID", required=False, )
    tosc = fields.Char(string="Violation submitting Time",required=False, placeholder="ساعة")
    tosc_1 = fields.Char(string=" ", required=False, placeholder="اللحظة" )
    am_pm_1 = fields.Selection(string=" ", selection=[('am', 'AM'), ('pm', 'PM'), ], required=False, )
    case_detail = fields.Text(string='Violation details ')
    case_type = fields.One2many('case.type1', "main_class", string="Violation Type")
    party_link = fields.One2many('traffic.party.detail', "main_class", string="Party Detail")
    receive_link = fields.One2many('traffic.receive', "main_class", string="Receiving Party")

    @api.model
    def create(self, vals):
        vals['number'] = self.env['ir.sequence'].next_by_code('record.number')
        vals['case_id'] = self.env['ir.sequence'].next_by_code('record.case')
        new_record = super(ViolationDetail, self).create(vals)
        return new_record

    @api.onchange('date')
    def _change_daytime(self):
        if self.date:
            self.day = datetime.datetime.strptime(self.date,'%Y-%m-%d').strftime('%A')
            self.time = (datetime.datetime.now() + timedelta(hours=5)).strftime("%I:%M:%S %p")
            # self.violation = (datetime.datetime.now() + timedelta(hours=5)).strftime("%I:%M:%S %p")
            # self.tosc = (datetime.datetime.now() + timedelta(hours=5)).strftime("%I:%M:%S %p")

    # def give_time(self):
    #     self.violation = (datetime.datetime.now() + timedelta(hours=5)).strftime("%I:%M:%S %p")
    #
    # def give_time1(self):
    #     self.tosc = (datetime.datetime.now() + timedelta(hours=5)).strftime("%I:%M:%S %p")


class TrafficReceive(models.Model):
    _name = 'traffic.receive'
    _rec_name = 'receiving_party'

    receiving_party = fields.Many2one('receiving.party', string="Receiving Party",required=False,)
    receiving_party_rank = fields.Many2one('receiving.party.rank', string="Receiving Party Rank",required=False,)
    receiving_name = fields.Char(string="Receiving Party Name",required=False,)

    main_class = fields.Many2one(comodel_name="violation.detail", string="Receiving Party", required=False, )


class trafficPartyDetail(models.Model):
    _name = 'traffic.party.detail'

    # party = fields.Text("Party")
    car_name = fields.Many2one('car.name',"Name of Car",required=False,)
    car_plate = fields.Char("Plate Number",required=False,)
    name = fields.Char("Driver Name",required=False,)
    driver_country = fields.Many2one('res.country', "Nationality",required=False,)
    id_num = fields.Char("ID number",required=True,)
    id_type = fields.Many2one('id.type', "ID Type",required=False,)
    sex = fields.Selection(string="Gender", selection=[('m', 'ذكر'), ('f', 'أنثى'), ],required=True, )
    dln = fields.Char("Driving License Number",required=False,)
    oftc = fields.Char("Owner of the car",required=False,)
    car_maker = fields.Many2one(comodel_name="car.maker", string="Maker of Car", required=False, )
    remark = fields.Text("Remarks",required=False,)
    other_onwer = fields.Boolean("Owner Is Someone Else ?")
    # vio_id = fields.Char("Violation Id")

    main_class = fields.Many2one('violation.detail')
    owner_detail = fields.One2many('owner.detail', 'main_class', string="Owner Detail")


class OwnerDetail(models.Model):
    _name = 'owner.detail'

    name = fields.Char("Name of Owner",required=False,)
    country = fields.Many2one('res.country', "Nationality of Owner",required=False,)
    id_num = fields.Char("ID number of Owner",required=False,)
    id_type = fields.Many2one('id.type', "ID Type of Owner",required=False,)
    mobile = fields.Char("Mobile Number of Owner",required=False,)
    remark = fields.Text("Remarks",required=False,)

    main_class = fields.Many2one('traffic.party.detail')


class MinistryName(models.Model):
    _name = 'ministry.name'

    name = fields.Char(string="Name of Ministry",required=True,)


class HospitalName(models.Model):
    _name = 'hospital.name'

    name = fields.Char(string="Name of Hospital",required=True,)


class MeanTrans(models.Model):
    _name = 'mean.trans'

    name = fields.Char(string="Means of Transportation",required=True,)


class WhatFound(models.Model):
    _name = 'what.found'

    name = fields.Char(string="What we found",required=True,)


class IDType(models.Model):
    _name = 'id.type'

    name = fields.Char(string="ID Type",required=True,)


class RoadName(models.Model):
    _name = 'road.name'

    name = fields.Char(string="Road Name",required=True,)
    road_tree = fields.One2many(comodel_name="road.tree", inverse_name="road", string="Road Link", required=False, )
    receiving_tree = fields.One2many(comodel_name="receiving.party", inverse_name="road_link", string="Road Link", required=False, )
    direction_tree = fields.One2many(comodel_name="road.tag", inverse_name="direction_link", string="Direction Link", required=False, )

    @api.model
    def create(self, val):
        record = super(RoadName, self).create(val)
        for x in record.road_tree:
            x.center.road_name = record.id
            for y in x.car_center_link:
                y.car_center = x.center
        for z in record.receiving_tree:
            z.road_name = record.id

        for x in record.direction_tree:
            x.direction.road_link = record.id
            for y in x.direction_tag_link:
                y.direction_name = x.direction

        return record

    @api.multi
    def write(self, val):
        super(RoadName, self).write(val)
        for x in self.road_tree:
            x.center.road_name = self.id
            for y in x.car_center_link:
                y.car_center = x.center
        for z in self.receiving_tree:
            z.road_name = self.id

        for x in self.direction_tree:
            x.direction.road_link = self.id
            for y in x.direction_tag_link:
                y.direction_name = x.direction

        return True


class RoadTree(models.Model):
    _name = 'road.tree'
    _rec_name = 'road'

    center = fields.Many2one(comodel_name="center.name", string="Center Name",required=True,)
    road = fields.Many2one(comodel_name="road.name", string="Road Tree",required=True,)
    car_center_link = fields.One2many(comodel_name="car.code", inverse_name="road_link", string="Car Center", required=False, )

class RoadTag(models.Model):
    _name = 'road.tag'
    _rec_name = 'direction_link'

    direction = fields.Many2one(comodel_name="direction.name", string="Direction Name",required=True,)
    direction_link = fields.Many2one(comodel_name="road.name", string="Road Tree",required=True,)
    direction_tag_link = fields.One2many(comodel_name="digital.tag", inverse_name="road_link", string="Direction Tag", required=False, )


class CenterName(models.Model):
    _name = 'center.name'

    name = fields.Char(string="Center Name",required=True,)
    road_name = fields.Many2one(comodel_name="road.name", string="Road Name", required=False, )


class Location(models.Model):
    _name = 'location.name'

    name = fields.Char(string="Location Name",required=True,)


class DigitalTag(models.Model):
    _name = 'digital.tag'

    name = fields.Char(string="Digital Tag",required=True,)
    direction_name = fields.Many2one(comodel_name="direction.name", string="Direction Name", required=False, )
    road_link = fields.Many2one(comodel_name="road.tag", string="Road Tree Link", required=False, )


class Direction(models.Model):
    _name = 'direction.name'

    name = fields.Char(string="Direction",required=True,)
    road_link = fields.Many2one(comodel_name="road.name", string="Road Name", required=False, )


class ReceivingParty(models.Model):
    _name = 'receiving.party'

    name = fields.Char(string="Receiving Party",required=True,)
    road_name  = fields.Many2one(comodel_name="road.name", string="Road Name", required=False, )
    road_link = fields.Many2one(comodel_name="road.name", string="Road Link", required=False, )

class ReceivingPartyRank(models.Model):
    _name = 'receiving.party.rank'

    name = fields.Char(string="Receiving Party Rank",required=True,)


class TypeOfCase(models.Model):
    _name = 'type.case'

    name = fields.Char(string="Type of Case",required=True,)
    case = fields.Many2one(comodel_name="main.case", string="Case", required=False, )


class TypeOfViolation(models.Model):
    _name = 'type.violation'

    name = fields.Char(string="Type of Violation",required=True,)


class CategoryCase(models.Model):
    _name = 'cate.case'

    name = fields.Char(string="Detail",required=True,)
    case_type = fields.Many2one(comodel_name="type.case", string="Case Type", required=False, )


class CarMaker(models.Model):
    _name = 'car.maker'

    name = fields.Char(string="Maker of Car",required=True,)


class CarName(models.Model):
    _name = 'car.name'

    name = fields.Char(string="Name of Car",required=True,)
    maker = fields.Many2one(comodel_name="car.maker", string="Car Maker", required=False, )

class CarColor(models.Model):
    _name = 'car.color'

    name = fields.Char(string="Color of Car",required=True,)

class CarModel(models.Model):
    _name = 'car.model'

    name = fields.Char(string="Model of Car",required=True,)

class CaseLevel(models.Model):
    _name = 'case.level'
    _rec_name = 'case'
    _description = "Create Case Level"

    case = fields.Many2one(comodel_name="main.case", string="Case",required=True,)
    tree_link = fields.One2many(comodel_name="case.level.tree", inverse_name="level_link", string="Case Type", required=False, )

    @api.model
    def create(self, val):
        record = super(CaseLevel, self).create(val)
        for x in record.tree_link:
            x.case_type.case = record.case
            for y in x.case_level_cate:
                y.case_cate.case_type = x.case_type
                for z  in y.case_level_sub_cate_link:
                    z.case_sub_cate.case_cate = y.case_cate

        return record

    @api.multi
    def write(self, val):
        super(CaseLevel, self).write(val)
        for x in self.tree_link:
            x.case_type.case = self.case
            for y in x.case_level_cate:
                y.case_cate.case_type = x.case_type
                for z  in y.case_level_sub_cate_link:
                    z.case_sub_cate.case_cate = y.case_cate
        return True


class CaseLevelTree(models.Model):
    _name = 'case.level.tree'
    _rec_name = 'case_type'

    level_link = fields.Many2one(comodel_name="case.level", string="Case Type",required=True,)
    case_type = fields.Many2one(comodel_name="type.case", string="Case Type",required=True, )
    case_level_cate = fields.One2many(comodel_name="case.level.cate", inverse_name="case_level_link", string="Case Level Detail", required=False, )


class CaseSubCate(models.Model):
    _name = 'case.sub.cate'
    _rec_name = 'name'
    _description = 'More Detail'

    name = fields.Char(string="More Detail",required=True,)
    case_cate = fields.Many2one(comodel_name="cate.case", string="Detail", required=False, )


class CaseLevelCate(models.Model):
    _name = 'case.level.cate'
    _rec_name = 'case_cate'

    case_cate = fields.Many2one(comodel_name="cate.case", string="Detail",required=True,)
    case_type = fields.Many2one(comodel_name="type.case", string="Case Type",required=True,)
    case_level_link = fields.Many2one(comodel_name="case.level.tree", string="Case Level Detail", required=False, )
    case_level_sub_cate_link = fields.One2many(comodel_name="case.level.cate.sub", inverse_name="case_cate_level_link", string="Case Level More Detail", required=False, )


class CaseLevelCateSub(models.Model):
    _name = 'case.level.cate.sub'
    _rec_name = 'case_sub_cate'

    case_cate = fields.Many2one(comodel_name="cate.case", string="Detail",required=True,)
    case_sub_cate = fields.Many2one(comodel_name="case.sub.cate", string="More Detail",required=True,)
    case_cate_level_link = fields.Many2one(comodel_name="case.level.cate", string="Case Level More Detail", required=False, )


class MainCase(models.Model):
    _name = 'main.case'
    _rec_name = 'name'

    name = fields.Char(string="Case",required=True,)



class CarCode(models.Model):
    _name = 'car.code'
    _rec_name = 'name'

    name = fields.Char(string="Code of Police CAR",required=True,)
    car_center = fields.Many2one(comodel_name="center.name", string="Center Name", required=False, )
    road_link = fields.Many2one(comodel_name="road.tree", string="Road Tree Link", required=False, )


class CarConfig(models.Model):
    _name = 'car.config'
    _rec_name = 'car_maker'

    car_maker = fields.Many2one(comodel_name="car.maker", string="Car Maker", required=True, )
    car_name_config = fields.One2many(comodel_name="car.name.config", inverse_name="car_config_link", string="Car Name Config", required=False, )

    @api.model
    def create(self, val):
        record = super(CarConfig, self).create(val)
        for x in record.car_name_config:
            x.name.maker = record.id
        return record

    @api.multi
    def write(self, val):
        super(CarConfig, self).write(val)
        for x in self.car_name_config:
            x.name.maker = self.id
        return True

class CarNameConfig(models.Model):
    _name = 'car.name.config'
    _rec_name = 'name'

    name = fields.Many2one(comodel_name="car.name", string="Car Name", required=True, )
    car_config_link = fields.Many2one(comodel_name="car.config", string="Car Name Config", required=False, )

class ModelColor(models.Model):
    _name = 'model.color'

    color = fields.One2many(comodel_name="color.conf", inverse_name="model_color", string="Color", required=False, )
    model = fields.One2many(comodel_name="model.conf", inverse_name="model_color", string="Model", required=False, )
    name = fields.Char(string="Colors And Model", default="Colors And Models", required=False, )

class ColorConf(models.Model):
    _name = 'color.conf'
    _rec_name = 'name'

    name = fields.Many2one(comodel_name="car.color", string="Color", required=False, )
    model_color = fields.Many2one(comodel_name="model.color", string="Color", required=False, )


class ModelConf(models.Model):
    _name = 'model.conf'
    _rec_name = 'name'

    name = fields.Many2one(comodel_name="car.model", string="Model", required=False, )
    model_color = fields.Many2one(comodel_name="model.color", string="Model", required=False, )


class IDTypeConfig(models.Model):
    _name = 'id.config'
    _rec_name = 'name'

    name = fields.Char(string="ID Type", default="ID Type and Other Configurations", required=False, )
    id_type = fields.One2many(comodel_name="idtype.conf", inverse_name="id_config", string="ID Type", required=False, )
    what_found = fields.One2many(comodel_name="what.conf", inverse_name="id_config", string="What We Found", required=False, )
    reason = fields.One2many(comodel_name="reason.conf", inverse_name="id_config", string="Accident Reasons", required=False, )
    result = fields.One2many(comodel_name="result.conf", inverse_name="id_config", string="Accident Results", required=False, )
    relation = fields.One2many(comodel_name="relation.conf", inverse_name="id_config", string="Relation", required=False, )


class IDConf(models.Model):
    _name = 'idtype.conf'
    _rec_name = 'name'

    name = fields.Char(string="ID Type", default="ID What Found and Other Configurations", required=False, )
    id_type = fields.Many2one(comodel_name="id.type", string="ID Type", required=True, )
    id_config = fields.Many2one(comodel_name="id.config", string="Id config", required=False, )

class WhatConf(models.Model):
    _name = 'what.conf'
    _rec_name = 'name'
    name = fields.Char(string="What We Found", default="ID What Found and Other Configurations", required=False, )
    what_found = fields.Many2one(comodel_name="type.case", string="What We Found", required=True, )
    id_config = fields.Many2one(comodel_name="id.config", string="Id config", required=False, )

class ReasonConf(models.Model):
    _name = 'reason.conf'
    _rec_name = 'name'
    name = fields.Char(string="Accident Reasons", default="ID What Found and Other Configurations", required=False, )
    reason = fields.Many2one(comodel_name="accident.reason", string="Accident Reasons", required=True, )
    id_config = fields.Many2one(comodel_name="id.config", string="Id config", required=False, )

class ResultConf(models.Model):
    _name = 'result.conf'
    _rec_name = 'name'
    name = fields.Char(string="Accident Results", default="ID What Found and Other Configurations", required=False, )
    result = fields.Many2one(comodel_name="accident.result", string="Accident Results", required=True, )
    id_config = fields.Many2one(comodel_name="id.config", string="Id config", required=False, )

class RelationConf(models.Model):
    _name = 'relation.conf'
    _rec_name = 'name'
    name = fields.Char(string="Relation", default="ID What Found and Other Configurations",required=False, )
    relation = fields.Many2one(comodel_name="accident.relation", string="Relation", required=True, )
    id_config = fields.Many2one(comodel_name="id.config", string="Id config", required=False, )


class AccidentReason(models.Model):
    _name = 'accident.reason'
    _rec_name = 'show_name'

    name = fields.Char(string="Accident Reason", required=True, )
    category = fields.Many2one(comodel_name="accident.category", string="Main Category", required=False, )
    show_name = fields.Char(string="show_name", required=False, )

    @api.onchange('name', 'category')
    def onchange_name_case(self):
        if self.name and self.category:
            self.show_name = self.name + "--" + self.category.name


class AccidentCategory(models.Model):
    _name = 'accident.category'

    name = fields.Char(string="Accident Reason Main Category", required=True, )


class AccidentResult(models.Model):
    _name = 'accident.result'
    _rec_name = 'show_name'

    name = fields.Char(string="Accident Result", required=True,)
    case = fields.Many2one(comodel_name="case.level", string="Result of Case", required=False, )
    show_name = fields.Char(string="show_name", required=False, )

    @api.onchange('name', 'case')
    def onchange_name_case(self):
        if self.name and self.case:
            self.show_name = self.name + "--" + self.case.case.name


class AccidentRelation(models.Model):
    _name = 'accident.relation'

    name = fields.Char(string="Relation", required=True,)


class RankConfig(models.Model):
    _name = 'rank.config'
    _rec_name = 'name'

    name = fields.Char(string="Ranks Configuration", default="Ranks Configuration", required=False, )
    of1_rank = fields.One2many(comodel_name="rank1.conf", inverse_name="id_config", string="Rank of Police Officer 1", required=False, )
    of2_rank = fields.One2many(comodel_name="rank2.conf", inverse_name="id_config", string="Rank of Police Officer 2", required=False, )
    rec_rank = fields.One2many(comodel_name="rankr.conf", inverse_name="id_config", string="Rank of Receiving Party", required=False, )


class RankOConf(models.Model):
    _name = 'rank1.conf'
    _rec_name = 'name'

    name = fields.Char(string="Ranks Configuration", default="Ranks Configuration", required=False, )
    of1_rank = fields.Many2one(comodel_name="rank.of1", string="Rank of Police Officer 1", required=True, )
    id_config = fields.Many2one(comodel_name="rank.config", string="Id config", required=False, )

class RankTConf(models.Model):
    _name = 'rank2.conf'
    _rec_name = 'name'

    name = fields.Char(string="Ranks Configuration", default="Ranks Configuration", required=False, )
    of2_rank = fields.Many2one(comodel_name="rank.of2", string="Rank of Police Officer 2", required=True, )
    id_config = fields.Many2one(comodel_name="rank.config", string="Id config", required=False, )

class RankRConf(models.Model):
    _name = 'rankr.conf'
    _rec_name = 'name'

    name = fields.Char(string="Ranks Configuration", default="Ranks Configuration", required=False, )
    rec_rank = fields.Many2one(comodel_name="receiving.party.rank", string="Rank of Receiving Party", required=True, )
    id_config = fields.Many2one(comodel_name="rank.config", string="Id config", required=False, )


class RankOf1(models.Model):
    _name = 'rank.of1'

    name = fields.Char(string="Rank of Police Officer 1" ,required=True,)

class RankOf2(models.Model):
    _name = 'rank.of2'

    name = fields.Char(string="Rank of Police Officer 2" ,required=True,)

#
# class NewPage(http.Controller):
#     @http.route('/police/',auth='public', website=True)
#     def index(self):
#         return http.request.render('police_project.index')
#
#
# class Websiste(Website):
#     @http.route(auth='public')
#     def index(self, data={},**kw):
#         super(Website, self).index(**kw)
#         return http.request.render('police_project.index', data)




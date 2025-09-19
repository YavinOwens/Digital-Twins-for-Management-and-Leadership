"""
ISO 19115 Metadata Management Tool

This module provides tools for creating, validating, and managing
ISO 19115 metadata for geospatial data in the Digital Twin system.
"""

from crewai.tools import tool
from typing import Dict, List, Any, Optional
import logging
import xml.etree.ElementTree as ET
from datetime import datetime
import json
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ISO19115MetadataManager:
    """
    Manages ISO 19115 metadata for geospatial data
    """
    
    def __init__(self):
        self.namespaces = {
            'gmd': 'http://www.isotc211.org/2005/gmd',
            'gco': 'http://www.isotc211.org/2005/gco',
            'gml': 'http://www.opengis.net/gml/3.2',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
        }
    
    def create_metadata_record(self, 
                             title: str,
                             abstract: str,
                             keywords: List[str],
                             spatial_extent: Dict[str, float],
                             temporal_extent: Dict[str, str],
                             data_type: str = "dataset",
                             contact_info: Dict[str, str] = None,
                             coordinate_system: str = "EPSG:4326",
                             resolution: str = None,
                             lineage: str = None) -> str:
        """
        Create ISO 19115 metadata record
        
        Args:
            title: Dataset title
            abstract: Dataset abstract/description
            keywords: List of keywords
            spatial_extent: Bounding box coordinates {west, east, south, north}
            temporal_extent: Temporal coverage {start_date, end_date}
            data_type: Type of data (dataset, series, service)
            contact_info: Contact information
            coordinate_system: Coordinate reference system
            resolution: Spatial resolution
            lineage: Data lineage information
            
        Returns:
            ISO 19115 XML metadata record
        """
        try:
            # Create root element
            root = ET.Element('gmd:MD_Metadata')
            root.set('xmlns:gmd', self.namespaces['gmd'])
            root.set('xmlns:gco', self.namespaces['gco'])
            root.set('xmlns:gml', self.namespaces['gml'])
            root.set('xmlns:xsi', self.namespaces['xsi'])
            root.set('xsi:schemaLocation', 
                    'http://www.isotc211.org/2005/gmd http://www.isotc211.org/2005/gmd/gmd.xsd')
            
            # File identifier
            file_id = ET.SubElement(root, 'gmd:fileIdentifier')
            file_id_gco = ET.SubElement(file_id, 'gco:CharacterString')
            file_id_gco.text = str(uuid.uuid4())
            
            # Language
            language = ET.SubElement(root, 'gmd:language')
            language_gco = ET.SubElement(language, 'gco:CharacterString')
            language_gco.text = 'eng'
            
            # Character set
            charset = ET.SubElement(root, 'gmd:characterSet')
            charset_code = ET.SubElement(charset, 'gmd:MD_CharacterSetCode')
            charset_code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_CharacterSetCode')
            charset_code.set('codeListValue', 'utf8')
            
            # Parent identifier
            parent_id = ET.SubElement(root, 'gmd:parentIdentifier')
            parent_id_gco = ET.SubElement(parent_id, 'gco:CharacterString')
            parent_id_gco.text = 'Digital Twin System'
            
            # Hierarchy level
            hierarchy = ET.SubElement(root, 'gmd:hierarchyLevel')
            hierarchy_code = ET.SubElement(hierarchy, 'gmd:MD_ScopeCode')
            hierarchy_code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_ScopeCode')
            hierarchy_code.set('codeListValue', data_type)
            
            # Contact information
            if contact_info:
                contact = ET.SubElement(root, 'gmd:contact')
                contact_info_elem = self._create_contact_info(contact_info)
                contact.append(contact_info_elem)
            
            # Date stamp
            date_stamp = ET.SubElement(root, 'gmd:dateStamp')
            date_stamp_gco = ET.SubElement(date_stamp, 'gco:DateTime')
            date_stamp_gco.text = datetime.now().isoformat()
            
            # Metadata standard name
            std_name = ET.SubElement(root, 'gmd:metadataStandardName')
            std_name_gco = ET.SubElement(std_name, 'gco:CharacterString')
            std_name_gco.text = 'ISO 19115:2003'
            
            # Metadata standard version
            std_version = ET.SubElement(root, 'gmd:metadataStandardVersion')
            std_version_gco = ET.SubElement(std_version, 'gco:CharacterString')
            std_version_gco.text = '2003'
            
            # Identification info
            id_info = ET.SubElement(root, 'gmd:identificationInfo')
            id_info_elem = self._create_identification_info(title, abstract, keywords, spatial_extent, temporal_extent, resolution)
            id_info.append(id_info_elem)
            
            # Distribution info
            dist_info = ET.SubElement(root, 'gmd:distributionInfo')
            dist_info_elem = self._create_distribution_info()
            dist_info.append(dist_info_elem)
            
            # Data quality info
            if lineage:
                quality_info = ET.SubElement(root, 'gmd:dataQualityInfo')
                quality_info_elem = self._create_quality_info(lineage)
                quality_info.append(quality_info_elem)
            
            # Convert to string
            xml_str = ET.tostring(root, encoding='unicode', method='xml')
            return xml_str
            
        except Exception as e:
            logger.error(f"Error creating ISO 19115 metadata: {e}")
            return f"Error creating metadata: {e}"
    
    def _create_contact_info(self, contact_info: Dict[str, str]) -> ET.Element:
        """Create contact information element"""
        contact_elem = ET.Element('gmd:CI_ResponsibleParty')
        
        # Individual name
        if 'individual_name' in contact_info:
            indiv_name = ET.SubElement(contact_elem, 'gmd:individualName')
            indiv_name_gco = ET.SubElement(indiv_name, 'gco:CharacterString')
            indiv_name_gco.text = contact_info['individual_name']
        
        # Organisation name
        if 'organisation_name' in contact_info:
            org_name = ET.SubElement(contact_elem, 'gmd:organisationName')
            org_name_gco = ET.SubElement(org_name, 'gco:CharacterString')
            org_name_gco.text = contact_info['organisation_name']
        
        # Contact info
        contact_details = ET.SubElement(contact_elem, 'gmd:contactInfo')
        contact_details_elem = ET.Element('gmd:CI_Contact')
        
        # Email
        if 'email' in contact_info:
            email = ET.SubElement(contact_details_elem, 'gmd:electronicMailAddress')
            email_gco = ET.SubElement(email, 'gco:CharacterString')
            email_gco.text = contact_info['email']
        
        contact_details.append(contact_details_elem)
        
        # Role
        role = ET.SubElement(contact_elem, 'gmd:role')
        role_code = ET.SubElement(role, 'gmd:CI_RoleCode')
        role_code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_RoleCode')
        role_code.set('codeListValue', 'pointOfContact')
        
        return contact_elem
    
    def _create_identification_info(self, title: str, abstract: str, keywords: List[str], 
                                  spatial_extent: Dict[str, float], temporal_extent: Dict[str, str], 
                                  resolution: str) -> ET.Element:
        """Create identification information element"""
        id_elem = ET.Element('gmd:MD_DataIdentification')
        
        # Citation
        citation = ET.SubElement(id_elem, 'gmd:citation')
        citation_elem = self._create_citation(title)
        citation.append(citation_elem)
        
        # Abstract
        abstract_elem = ET.SubElement(id_elem, 'gmd:abstract')
        abstract_gco = ET.SubElement(abstract_elem, 'gco:CharacterString')
        abstract_gco.text = abstract
        
        # Purpose
        purpose = ET.SubElement(id_elem, 'gmd:purpose')
        purpose_gco = ET.SubElement(purpose, 'gco:CharacterString')
        purpose_gco.text = 'Digital Twin System Data'
        
        # Status
        status = ET.SubElement(id_elem, 'gmd:status')
        status_code = ET.SubElement(status, 'gmd:MD_ProgressCode')
        status_code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_ProgressCode')
        status_code.set('codeListValue', 'completed')
        
        # Keywords
        if keywords:
            keyword_elem = ET.SubElement(id_elem, 'gmd:descriptiveKeywords')
            keyword_elem_elem = ET.Element('gmd:MD_Keywords')
            
            for keyword in keywords:
                keyword_item = ET.SubElement(keyword_elem_elem, 'gmd:keyword')
                keyword_item_gco = ET.SubElement(keyword_item, 'gco:CharacterString')
                keyword_item_gco.text = keyword
            
            keyword_elem.append(keyword_elem_elem)
        
        # Resource constraints
        constraints = ET.SubElement(id_elem, 'gmd:resourceConstraints')
        constraints_elem = ET.Element('gmd:MD_LegalConstraints')
        
        # Use limitations
        use_lim = ET.SubElement(constraints_elem, 'gmd:useLimitation')
        use_lim_gco = ET.SubElement(use_lim, 'gco:CharacterString')
        use_lim_gco.text = 'Digital Twin System Use Only'
        
        constraints.append(constraints_elem)
        
        # Spatial representation type
        spatial_rep = ET.SubElement(id_elem, 'gmd:spatialRepresentationType')
        spatial_rep_code = ET.SubElement(spatial_rep, 'gmd:MD_SpatialRepresentationTypeCode')
        spatial_rep_code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_SpatialRepresentationTypeCode')
        spatial_rep_code.set('codeListValue', 'vector')
        
        # Spatial resolution
        if resolution:
            spatial_res = ET.SubElement(id_elem, 'gmd:spatialResolution')
            spatial_res_elem = ET.Element('gmd:MD_Resolution')
            
            distance = ET.SubElement(spatial_res_elem, 'gmd:distance')
            distance_gco = ET.SubElement(distance, 'gco:Distance')
            distance_gco.text = resolution
            
            spatial_res.append(spatial_res_elem)
        
        # Language
        language = ET.SubElement(id_elem, 'gmd:language')
        language_gco = ET.SubElement(language, 'gco:CharacterString')
        language_gco.text = 'eng'
        
        # Character set
        charset = ET.SubElement(id_elem, 'gmd:characterSet')
        charset_code = ET.SubElement(charset, 'gmd:MD_CharacterSetCode')
        charset_code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_CharacterSetCode')
        charset_code.set('codeListValue', 'utf8')
        
        # Topic category
        topic_cat = ET.SubElement(id_elem, 'gmd:topicCategory')
        topic_cat_elem = ET.SubElement(topic_cat, 'gmd:MD_TopicCategoryCode')
        topic_cat_elem.text = 'location'
        
        # Extent
        extent = ET.SubElement(id_elem, 'gmd:extent')
        extent_elem = self._create_extent(spatial_extent, temporal_extent)
        extent.append(extent_elem)
        
        return id_elem
    
    def _create_citation(self, title: str) -> ET.Element:
        """Create citation element"""
        citation_elem = ET.Element('gmd:CI_Citation')
        
        # Title
        title_elem = ET.SubElement(citation_elem, 'gmd:title')
        title_gco = ET.SubElement(title_elem, 'gco:CharacterString')
        title_gco.text = title
        
        # Date
        date_elem = ET.SubElement(citation_elem, 'gmd:date')
        date_elem_elem = ET.Element('gmd:CI_Date')
        
        date_item = ET.SubElement(date_elem_elem, 'gmd:date')
        date_item_gco = ET.SubElement(date_item, 'gco:Date')
        date_item_gco.text = datetime.now().strftime('%Y-%m-%d')
        
        date_type = ET.SubElement(date_elem_elem, 'gmd:dateType')
        date_type_code = ET.SubElement(date_type, 'gmd:CI_DateTypeCode')
        date_type_code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_DateTypeCode')
        date_type_code.set('codeListValue', 'creation')
        
        date_elem.append(date_elem_elem)
        
        return citation_elem
    
    def _create_extent(self, spatial_extent: Dict[str, float], temporal_extent: Dict[str, str]) -> ET.Element:
        """Create extent element"""
        extent_elem = ET.Element('gmd:EX_Extent')
        
        # Geographic extent
        geo_extent = ET.SubElement(extent_elem, 'gmd:geographicElement')
        geo_extent_elem = ET.Element('gmd:EX_GeographicBoundingBox')
        
        # West bound
        west_bound = ET.SubElement(geo_extent_elem, 'gmd:westBoundLongitude')
        west_bound_gco = ET.SubElement(west_bound, 'gco:Decimal')
        west_bound_gco.text = str(spatial_extent['west'])
        
        # East bound
        east_bound = ET.SubElement(geo_extent_elem, 'gmd:eastBoundLongitude')
        east_bound_gco = ET.SubElement(east_bound, 'gco:Decimal')
        east_bound_gco.text = str(spatial_extent['east'])
        
        # South bound
        south_bound = ET.SubElement(geo_extent_elem, 'gmd:southBoundLatitude')
        south_bound_gco = ET.SubElement(south_bound, 'gco:Decimal')
        south_bound_gco.text = str(spatial_extent['south'])
        
        # North bound
        north_bound = ET.SubElement(geo_extent_elem, 'gmd:northBoundLatitude')
        north_bound_gco = ET.SubElement(north_bound, 'gco:Decimal')
        north_bound_gco.text = str(spatial_extent['north'])
        
        geo_extent.append(geo_extent_elem)
        
        # Temporal extent
        if temporal_extent:
            temp_extent = ET.SubElement(extent_elem, 'gmd:temporalElement')
            temp_extent_elem = ET.Element('gmd:EX_TemporalExtent')
            
            extent_time = ET.SubElement(temp_extent_elem, 'gmd:extent')
            extent_time_elem = ET.Element('gml:TimePeriod')
            extent_time_elem.set('gml:id', 'temporal_extent')
            
            begin_time = ET.SubElement(extent_time_elem, 'gml:beginPosition')
            begin_time.text = temporal_extent['start_date']
            
            end_time = ET.SubElement(extent_time_elem, 'gml:endPosition')
            end_time.text = temporal_extent['end_date']
            
            extent_time.append(extent_time_elem)
            temp_extent.append(temp_extent_elem)
        
        return extent_elem
    
    def _create_distribution_info(self) -> ET.Element:
        """Create distribution information element"""
        dist_elem = ET.Element('gmd:MD_Distribution')
        
        # Distribution format
        format_elem = ET.SubElement(dist_elem, 'gmd:distributionFormat')
        format_elem_elem = ET.Element('gmd:MD_Format')
        
        format_name = ET.SubElement(format_elem_elem, 'gmd:name')
        format_name_gco = ET.SubElement(format_name, 'gco:CharacterString')
        format_name_gco.text = 'Digital Twin Data Format'
        
        format_version = ET.SubElement(format_elem_elem, 'gmd:version')
        format_version_gco = ET.SubElement(format_version, 'gco:CharacterString')
        format_version_gco.text = '1.0'
        
        format_elem.append(format_elem_elem)
        
        return dist_elem
    
    def _create_quality_info(self, lineage: str) -> ET.Element:
        """Create data quality information element"""
        quality_elem = ET.Element('gmd:DQ_DataQuality')
        
        # Scope
        scope = ET.SubElement(quality_elem, 'gmd:scope')
        scope_elem = ET.Element('gmd:DQ_Scope')
        
        level = ET.SubElement(scope_elem, 'gmd:level')
        level_code = ET.SubElement(level, 'gmd:MD_ScopeCode')
        level_code.set('codeList', 'http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_ScopeCode')
        level_code.set('codeListValue', 'dataset')
        
        scope.append(scope_elem)
        
        # Lineage
        lineage_elem = ET.SubElement(quality_elem, 'gmd:lineage')
        lineage_elem_elem = ET.Element('gmd:LI_Lineage')
        
        statement = ET.SubElement(lineage_elem_elem, 'gmd:statement')
        statement_gco = ET.SubElement(statement, 'gco:CharacterString')
        statement_gco.text = lineage
        
        lineage_elem.append(lineage_elem_elem)
        
        return quality_elem
    
    def validate_metadata(self, metadata_xml: str) -> Dict[str, Any]:
        """
        Validate ISO 19115 metadata record
        
        Args:
            metadata_xml: XML metadata record
            
        Returns:
            Validation result
        """
        try:
            # Parse XML
            root = ET.fromstring(metadata_xml)
            
            # Check required elements
            required_elements = [
                'gmd:fileIdentifier',
                'gmd:language',
                'gmd:characterSet',
                'gmd:hierarchyLevel',
                'gmd:dateStamp',
                'gmd:metadataStandardName',
                'gmd:metadataStandardVersion',
                'gmd:identificationInfo'
            ]
            
            missing_elements = []
            for element in required_elements:
                if root.find(f'.//{element}') is None:
                    missing_elements.append(element)
            
            # Check identification info
            id_info = root.find('.//gmd:identificationInfo', self.namespaces)
            id_issues = []
            if id_info is not None:
                id_elem = id_info.find('gmd:MD_DataIdentification', self.namespaces)
                if id_elem is not None:
                    if id_elem.find('.//gmd:title', self.namespaces) is None:
                        id_issues.append('Missing title')
                    if id_elem.find('.//gmd:abstract', self.namespaces) is None:
                        id_issues.append('Missing abstract')
                    if id_elem.find('.//gmd:extent', self.namespaces) is None:
                        id_issues.append('Missing extent')
            
            # Validation result
            is_valid = len(missing_elements) == 0 and len(id_issues) == 0
            
            return {
                'valid': is_valid,
                'missing_elements': missing_elements,
                'identification_issues': id_issues,
                'total_issues': len(missing_elements) + len(id_issues)
            }
            
        except ET.ParseError as e:
            return {
                'valid': False,
                'error': f'XML parsing error: {e}',
                'missing_elements': [],
                'identification_issues': [],
                'total_issues': 1
            }
        except Exception as e:
            logger.error(f"Error validating metadata: {e}")
            return {
                'valid': False,
                'error': str(e),
                'missing_elements': [],
                'identification_issues': [],
                'total_issues': 1
            }


# Global metadata manager instance
metadata_manager = ISO19115MetadataManager()


@tool("create_iso19115_metadata")
def create_iso19115_metadata(title: str, abstract: str, keywords: List[str], 
                           spatial_extent: Dict[str, float], temporal_extent: Dict[str, str] = None,
                           data_type: str = "dataset", contact_info: Dict[str, str] = None,
                           resolution: str = None, lineage: str = None) -> str:
    """
    Create ISO 19115 metadata record for geospatial data.
    
    Args:
        title: Dataset title
        abstract: Dataset abstract/description
        keywords: List of keywords
        spatial_extent: Bounding box coordinates {west, east, south, north}
        temporal_extent: Temporal coverage {start_date, end_date}
        data_type: Type of data (dataset, series, service)
        contact_info: Contact information
        resolution: Spatial resolution
        lineage: Data lineage information
        
    Returns:
        ISO 19115 XML metadata record
    """
    try:
        metadata_xml = metadata_manager.create_metadata_record(
            title=title,
            abstract=abstract,
            keywords=keywords,
            spatial_extent=spatial_extent,
            temporal_extent=temporal_extent or {},
            data_type=data_type,
            contact_info=contact_info or {},
            resolution=resolution,
            lineage=lineage
        )
        
        return f"✅ ISO 19115 metadata created successfully!\n\n**Metadata Record:**\n```xml\n{metadata_xml}\n```"
        
    except Exception as e:
        logger.error(f"Error creating ISO 19115 metadata: {e}")
        return f"❌ Error creating metadata: {e}"


@tool("validate_iso19115_metadata")
def validate_iso19115_metadata(metadata_xml: str) -> str:
    """
    Validate ISO 19115 metadata record.
    
    Args:
        metadata_xml: XML metadata record to validate
        
    Returns:
        Validation result with issues and recommendations
    """
    try:
        validation_result = metadata_manager.validate_metadata(metadata_xml)
        
        report = f"🔍 **ISO 19115 Metadata Validation Report**\n\n"
        
        if validation_result['valid']:
            report += "✅ **Status: VALID**\n\n"
            report += "The metadata record meets ISO 19115 standards and contains all required elements."
        else:
            report += "❌ **Status: INVALID**\n\n"
            
            if validation_result.get('missing_elements'):
                report += "**Missing Required Elements:**\n"
                for element in validation_result['missing_elements']:
                    report += f"- {element}\n"
                report += "\n"
            
            if validation_result.get('identification_issues'):
                report += "**Identification Issues:**\n"
                for issue in validation_result['identification_issues']:
                    report += f"- {issue}\n"
                report += "\n"
            
            if validation_result.get('error'):
                report += f"**Error:** {validation_result['error']}\n\n"
        
        report += f"**Total Issues:** {validation_result['total_issues']}\n"
        
        if not validation_result['valid']:
            report += "\n**Recommendations:**\n"
            report += "1. Add missing required elements\n"
            report += "2. Ensure proper identification information\n"
            report += "3. Validate XML structure and namespaces\n"
            report += "4. Check element content and formatting\n"
        
        return report
        
    except Exception as e:
        logger.error(f"Error validating ISO 19115 metadata: {e}")
        return f"❌ Error validating metadata: {e}"


@tool("extract_geospatial_metadata")
def extract_geospatial_metadata(data_description: str) -> str:
    """
    Extract geospatial metadata information from data description.
    
    Args:
        data_description: Description of the geospatial data
        
    Returns:
        Extracted metadata information
    """
    try:
        report = f"🌍 **Geospatial Metadata Extraction**\n\n"
        report += f"**Data Description:** {data_description}\n\n"
        
        # Extract potential spatial information
        spatial_info = []
        if 'latitude' in data_description.lower() or 'longitude' in data_description.lower():
            spatial_info.append("Coordinate information detected")
        if 'bounding box' in data_description.lower() or 'bbox' in data_description.lower():
            spatial_info.append("Bounding box information detected")
        if 'projection' in data_description.lower() or 'crs' in data_description.lower():
            spatial_info.append("Coordinate reference system information detected")
        if 'resolution' in data_description.lower() or 'scale' in data_description.lower():
            spatial_info.append("Spatial resolution information detected")
        
        # Extract potential temporal information
        temporal_info = []
        if 'date' in data_description.lower() or 'time' in data_description.lower():
            temporal_info.append("Temporal information detected")
        if 'year' in data_description.lower():
            temporal_info.append("Year information detected")
        if 'period' in data_description.lower() or 'range' in data_description.lower():
            temporal_info.append("Temporal period information detected")
        
        # Extract potential thematic information
        thematic_info = []
        if 'land use' in data_description.lower():
            thematic_info.append("Land use data")
        if 'population' in data_description.lower():
            thematic_info.append("Population data")
        if 'environment' in data_description.lower() or 'climate' in data_description.lower():
            thematic_info.append("Environmental data")
        if 'infrastructure' in data_description.lower():
            thematic_info.append("Infrastructure data")
        
        if spatial_info:
            report += "**Spatial Information:**\n"
            for info in spatial_info:
                report += f"- {info}\n"
            report += "\n"
        
        if temporal_info:
            report += "**Temporal Information:**\n"
            for info in temporal_info:
                report += f"- {info}\n"
            report += "\n"
        
        if thematic_info:
            report += "**Thematic Information:**\n"
            for info in thematic_info:
                report += f"- {info}\n"
            report += "\n"
        
        report += "**Recommendations for ISO 19115 Metadata:**\n"
        report += "1. Define spatial extent (bounding box coordinates)\n"
        report += "2. Specify coordinate reference system\n"
        report += "3. Add temporal coverage information\n"
        report += "4. Include thematic keywords\n"
        report += "5. Provide data lineage information\n"
        report += "6. Specify spatial resolution\n"
        report += "7. Add contact information\n"
        
        return report
        
    except Exception as e:
        logger.error(f"Error extracting geospatial metadata: {e}")
        return f"❌ Error extracting metadata: {e}"

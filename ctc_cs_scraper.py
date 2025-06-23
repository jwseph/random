#!/usr/bin/env python3
"""
CTC Link CS Course Scraper for Summer 2025
Focused scraper for Computer Science courses from Washington State Community Colleges
"""

import json
import csv
import time
import re
from datetime import datetime
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CTCCScourseScraper:
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        
        # Correct institution codes from the actual system
        self.wa_institutions = {
            'WA080': 'Bellevue College',
            'WA050': 'Everett Community College',
            'WA062': 'Seattle Central College',
            'WA063': 'North Seattle College',
            'WA064': 'South Seattle College',
            'WA070': 'Shoreline Community College',
            'WA100': 'Green River College',
            'WA110': 'Pierce College',
            'WA230': 'Edmonds College',
            'WA240': 'South Puget Sound Comm College',
            'WA171': 'Spokane CC',
            'WA172': 'Spokane Falls CC',
            'WA220': 'Tacoma CC',
            'WA260': 'Lake Washington Inst. of Tech.',
            'WA270': 'Renton Technical College'
        }
        
        self.base_url = "https://csprd.ctclink.us"
        self.courses_data = []
        self.setup_selenium()
    
    def setup_selenium(self):
        """Set up Selenium WebDriver"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("Selenium WebDriver initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Selenium: {e}")
            raise
    
    def close_driver(self):
        if self.driver:
            self.driver.quit()
    
    def navigate_to_cs_search(self, institution_code):
        """Navigate to CS course search page - two step process"""
        try:
            # Step 1: First access the institution-specific URL
            institution_url = f"{self.base_url}/psc/csprd/EMPLOYEE/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_Main?institution={institution_code}"
            logger.info(f"Step 1: Accessing institution URL for {institution_code}")
            
            self.driver.get(institution_url)
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Wait a moment for the institution context to be established
            time.sleep(2)
            
            # Step 2: Now access the CS-specific URL
            cs_org_code = f"{institution_code[2:]}CS"  # WA080 -> 080CS
            cs_url = f"{self.base_url}/psc/csprd/EMPLOYEE/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_Main?acad_org={cs_org_code}"
            logger.info(f"Step 2: Accessing CS URL with filter {cs_org_code}")
            
            self.driver.get(cs_url)
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Switch to iframe - try multiple methods
            iframe_found = False
            
            # Method 1: Try by name
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.frame_to_be_available_and_switch_to_it((By.NAME, "TargetContent"))
                )
                logger.info("✓ Switched to TargetContent iframe by name")
                iframe_found = True
            except TimeoutException:
                pass
            
            # Method 2: Try by ID
            if not iframe_found:
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.frame_to_be_available_and_switch_to_it((By.ID, "main_iframe"))
                    )
                    logger.info("✓ Switched to iframe by ID")
                    iframe_found = True
                except TimeoutException:
                    pass
            
            # Method 3: Find any iframe
            if not iframe_found:
                iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                logger.info(f"Found {len(iframes)} iframe(s) on page")
                
                for i, iframe in enumerate(iframes):
                    try:
                        self.driver.switch_to.frame(iframe)
                        logger.info(f"✓ Switched to iframe #{i}")
                        iframe_found = True
                        break
                    except:
                        continue
            
            if not iframe_found:
                logger.info("No iframe found, using main frame")
            
            return True
            
        except Exception as e:
            logger.error(f"Error navigating to {institution_code}: {e}")
            return False
    
    def set_summer_2025_term(self):
        """Set term to Summer 2025 by typing into input field"""
        try:
            # Wait for page to fully load
            time.sleep(3)
            
            # First try to find input fields that might contain term information
            input_elements = self.driver.find_elements(By.TAG_NAME, "input")
            logger.info(f"Found {len(input_elements)} input elements on page")
            
            # Look for input fields that might contain term data
            term_candidates = []
            
            for input_element in input_elements:
                try:
                    input_value = input_element.get_attribute('value') or ''
                    input_placeholder = input_element.get_attribute('placeholder') or ''
                    input_name = input_element.get_attribute('name') or ''
                    input_id = input_element.get_attribute('id') or ''
                    input_type = input_element.get_attribute('type') or 'text'
                    
                    # Look for inputs that contain term-like data or names
                    all_text = f"{input_value} {input_placeholder} {input_name} {input_id}".upper()
                    
                    # Check if this might be a term field
                    if (any(term_indicator in all_text for term_indicator in ['TERM', 'STRM', 'SPRING', 'SUMMER', 'FALL']) or
                        any(year in input_value for year in ['2024', '2025', '2026']) or
                        input_type.lower() in ['text', 'search']):
                        
                        term_candidates.append({
                            'element': input_element,
                            'value': input_value,
                            'placeholder': input_placeholder,
                            'name': input_name,
                            'id': input_id,
                            'type': input_type
                        })
                        
                        logger.info(f"Term candidate: value='{input_value}' name='{input_name}' id='{input_id}' type='{input_type}'")
                
                except Exception as e:
                    continue
            
            # Try to set "SUMMER 2025" in the most promising input field
            for candidate in term_candidates:
                try:
                    element = candidate['element']
                    
                    # Skip if not visible or not enabled
                    if not element.is_displayed() or not element.is_enabled():
                        continue
                    
                    # Clear the field and type "SUMMER 2025"
                    element.clear()
                    time.sleep(0.5)  # Brief pause after clearing
                    
                    # Type "SUMMER 2025"
                    element.send_keys("SUMMER 2025")
                    time.sleep(1)  # Wait for autocomplete
                    
                    # Press Enter to confirm selection if there's autocomplete
                    element.send_keys(Keys.ENTER)
                    time.sleep(0.5)
                    
                    # Verify the value was set
                    new_value = element.get_attribute('value')
                    logger.info(f"✓ Set term field to: '{new_value}' (name='{candidate['name']}', id='{candidate['id']}')")
                    
                    if "SUMMER" in new_value.upper() and "2025" in new_value:
                        return True
                    
                    # If that didn't work, try just "SUMMER" and see if autocomplete kicks in
                    element.clear()
                    time.sleep(0.5)
                    element.send_keys("SUMMER")
                    time.sleep(1)
                    
                    # Look for dropdown suggestions and select one with 2025
                    try:
                        # Check if autocomplete dropdown appeared
                        dropdown_options = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'suggestion') or contains(@class, 'dropdown') or contains(@class, 'option')]")
                        for option in dropdown_options:
                            if "2025" in option.text and "SUMMER" in option.text.upper():
                                option.click()
                                logger.info(f"✓ Selected from autocomplete: {option.text}")
                                return True
                    except:
                        pass
                    
                    # Final verification
                    final_value = element.get_attribute('value')
                    if "SUMMER" in final_value.upper():
                        logger.info(f"✓ Set term to: {final_value}")
                        return True
                
                except Exception as e:
                    logger.debug(f"Failed to set term in candidate: {e}")
                    continue
            
            # Fallback: try select dropdowns
            select_elements = self.driver.find_elements(By.TAG_NAME, "select")
            logger.info(f"Fallback: Found {len(select_elements)} select elements")
            
            for select_element in select_elements:
                try:
                    select = Select(select_element)
                    
                    # Look for Summer 2025 option
                    for option in select.options:
                        option_text = option.text.upper()
                        option_value = option.get_attribute('value')
                        
                        if (('SUMMER' in option_text and '2025' in option_text) or
                            '2255' in option_value or '2255' in option_text):
                            select.select_by_value(option_value)
                            logger.info(f"✓ Selected Summer 2025 from dropdown: {option_text}")
                            return True
                    
                    # If no Summer 2025, select first available term
                    if len(select.options) > 1:
                        select.select_by_index(1)
                        selected_text = select.first_selected_option.text
                        logger.info(f"✓ Selected first available term: {selected_text}")
                        return True
                        
                except Exception as e:
                    logger.debug(f"Error with select element: {e}")
                    continue
            
            logger.warning("Could not find or set term to SUMMER 2025")
            return False
            
        except Exception as e:
            logger.error(f"Error setting term: {e}")
            return False
    
    def click_search_button(self):
        """Click search button - find ANY button with 'Search' text"""
        try:
            # Wait for page to load
            time.sleep(2)
            
            # Find ALL clickable elements
            clickable_elements = self.driver.find_elements(By.XPATH, "//input | //button | //a")
            logger.info(f"Found {len(clickable_elements)} clickable elements")
            
            # Look for any element with "Search" in its text, value, or attributes
            search_candidates = []
            
            for element in clickable_elements:
                try:
                    # Check various attributes and text
                    element_text = element.text.upper()
                    element_value = element.get_attribute('value') or ''
                    element_title = element.get_attribute('title') or ''
                    element_id = element.get_attribute('id') or ''
                    element_name = element.get_attribute('name') or ''
                    
                    # Combine all text to search
                    all_text = f"{element_text} {element_value} {element_title} {element_id} {element_name}".upper()
                    
                    if 'SEARCH' in all_text:
                        search_candidates.append({
                            'element': element,
                            'text': element_text,
                            'value': element_value,
                            'id': element_id,
                            'name': element_name
                        })
                        logger.info(f"Search candidate: text='{element_text}' value='{element_value}' id='{element_id}'")
                
                except Exception as e:
                    continue
            
            # Try clicking the most promising search button
            for candidate in search_candidates:
                try:
                    element = candidate['element']
                    if element.is_enabled() and element.is_displayed():
                        element.click()
                        logger.info(f"✓ Clicked search button: {candidate}")
                        time.sleep(5)  # Wait longer for results to load
                        return True
                except Exception as e:
                    logger.debug(f"Failed to click candidate: {e}")
                    continue
            
            logger.warning("No working search button found")
            return False
            
        except Exception as e:
            logger.error(f"Error clicking search: {e}")
            return False
    
    def extract_course_data(self, institution_code, institution_name):
        """Extract CS course data from Material-UI structure"""
        courses = []
        
        try:
            # Wait for content to load
            time.sleep(3)
            
            # Check what's actually on the page
            page_text = self.driver.page_source
            logger.info(f"Page length: {len(page_text)} characters")
            
            # Parse with BeautifulSoup for better HTML structure handling
            soup = BeautifulSoup(page_text, 'html.parser')
            
            # Method 1: Look for Material-UI course headers (like "Technology and Computer Science | CS 101")
            course_headers = soup.find_all('h2', string=lambda text: text and 'CS ' in text and '|' in text)
            logger.info(f"Found {len(course_headers)} course headers with CS numbers")
            
            for header in course_headers:
                try:
                    header_text = header.get_text().strip()
                    
                    # Parse "Course Title | CS 101" format
                    if '|' in header_text:
                        parts = header_text.split('|')
                        if len(parts) >= 2:
                            course_title = parts[0].strip()
                            cs_part = parts[1].strip()
                            
                            # Extract course number (like "CS 101")
                            cs_match = re.search(r'CS\s+(\d+[A-Z]*)', cs_part, re.IGNORECASE)
                            if cs_match:
                                course_number = cs_match.group(1)
                                
                                # Find associated course sections 
                                sections = []
                                
                                # Look for the course container and find section cards
                                course_container = header.find_parent()
                                if course_container:
                                    # Find section cards (Material-UI cards with class info)
                                    section_cards = course_container.find_next_siblings()
                                    for sibling in section_cards[:10]:  # Limit search to avoid going too far
                                        if sibling.name and 'class' in sibling.attrs:
                                            # Look for section information in this card
                                            section_info = self.extract_section_info(sibling)
                                            if section_info:
                                                sections.append(section_info)
                                        
                                        # Stop if we hit another course header
                                        if sibling.find('h2'):
                                            break
                                
                                # Create course entry
                                course_data = {
                                    'institution_code': institution_code,
                                    'institution_name': institution_name,
                                    'scraped_at': datetime.now().isoformat(),
                                    'course_number': f"CS {course_number}",
                                    'title': course_title,
                                    'sections': sections,
                                    'raw_header': header_text
                                }
                                
                                courses.append(course_data)
                                logger.info(f"✓ Found CS course: CS {course_number} - {course_title} ({len(sections)} sections)")
                
                except Exception as e:
                    logger.debug(f"Error processing header: {e}")
                    continue
            
            # Method 2: Look for CS course patterns in any text content
            if not courses:
                logger.info("No Material-UI headers found, trying text pattern matching")
                body_text = soup.get_text()
                
                # Look for course title patterns
                course_patterns = [
                    r'([^|]+)\s*\|\s*CS\s+(\d+[A-Z]*)',  # "Title | CS 101"
                    r'CS\s+(\d+[A-Z]*)\s*[-:]\s*([^|]+)',  # "CS 101: Title"
                    r'Computer Science\s+(\d+[A-Z]*)\s*[-:]\s*([^|]+)'  # "Computer Science 101: Title"
                ]
                
                for pattern in course_patterns:
                    matches = re.findall(pattern, body_text, re.IGNORECASE | re.MULTILINE)
                    for match in matches:
                        if len(match) == 2:
                            if pattern.startswith(r'([^|]+)'):  # Title | CS format
                                title, number = match
                            else:  # CS Number: Title format
                                number, title = match
                            
                            course_data = {
                                'institution_code': institution_code,
                                'institution_name': institution_name,
                                'scraped_at': datetime.now().isoformat(),
                                'course_number': f"CS {number}",
                                'title': title.strip(),
                                'sections': [],
                                'extraction_method': 'text_pattern'
                            }
                            
                            courses.append(course_data)
                            logger.info(f"✓ Found CS course: CS {number} - {title.strip()}")
            
            # Method 3: Search for any mention of CS courses in the entire page
            if not courses:
                logger.info("No structured courses found, searching for any CS mentions")
                
                # Look for lines containing CS course numbers
                lines = body_text.split('\n')
                cs_lines = []
                
                for line in lines:
                    line = line.strip()
                    if re.search(r'\bCS\s+\d+\b', line, re.IGNORECASE) and len(line) > 5:
                        cs_lines.append(line)
                
                logger.info(f"Found {len(cs_lines)} lines with CS course numbers")
                
                # Extract unique course numbers
                found_numbers = set()
                for line in cs_lines:
                    matches = re.findall(r'\bCS\s+(\d+[A-Z]*)\b', line, re.IGNORECASE)
                    for number in matches:
                        if number not in found_numbers:
                            found_numbers.add(number)
                            
                            # Try to extract title from the same line
                            title = line
                            if '|' in line:
                                parts = line.split('|')
                                for part in parts:
                                    if f"CS {number}" not in part.upper():
                                        title = part.strip()
                                        break
                            
                            course_data = {
                                'institution_code': institution_code,
                                'institution_name': institution_name,
                                'scraped_at': datetime.now().isoformat(),
                                'course_number': f"CS {number}",
                                'title': title[:100],  # Limit title length
                                'sections': [],
                                'raw_line': line,
                                'extraction_method': 'text_search'
                            }
                            
                            courses.append(course_data)
                            logger.info(f"✓ Found CS course: CS {number}")
            
            # Log summary
            logger.info(f"Total CS courses found: {len(courses)}")
            if courses:
                course_numbers = [course['course_number'] for course in courses]
                logger.info(f"Course numbers: {', '.join(sorted(course_numbers))}")
            
        except Exception as e:
            logger.error(f"Error extracting course data: {e}")
        
        return courses
    
    def extract_section_info(self, element):
        """Extract section information from a course card element"""
        try:
            section_info = {}
            text = element.get_text()
            
            # Look for section indicators
            section_patterns = [
                r'Section\s*:?\s*([A-Z0-9]+)',
                r'([A-Z0-9]+)-([A-Z]+)\s*\(\s*(\d+)\s*\)',  # "AA-LEC (11055)"
            ]
            
            for pattern in section_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    if len(match.groups()) >= 3:  # Format like "AA-LEC (11055)"
                        section_info['section'] = match.group(1)
                        section_info['type'] = match.group(2)
                        section_info['class_number'] = match.group(3)
                    else:
                        section_info['section'] = match.group(1)
                    break
            
            # Look for instructor
            instructor_match = re.search(r'Instructor\s*:?\s*([^|]+?)(?:\s*Days|$)', text, re.IGNORECASE)
            if instructor_match:
                section_info['instructor'] = instructor_match.group(1).strip()
            
            # Look for days/times
            days_match = re.search(r'Days\s*:?\s*([^|]+?)(?:\s*Start|$)', text, re.IGNORECASE)
            if days_match:
                section_info['days'] = days_match.group(1).strip()
            
            # Look for dates
            dates_match = re.search(r'(\d{2}/\d{2}\s*-\s*\d{2}/\d{2})', text)
            if dates_match:
                section_info['dates'] = dates_match.group(1)
            
            return section_info if section_info else None
            
        except Exception as e:
            logger.debug(f"Error extracting section info: {e}")
            return None
    
    def scrape_institution(self, institution_code):
        """Scrape one institution"""
        institution_name = self.wa_institutions.get(institution_code)
        logger.info(f"Scraping {institution_name} ({institution_code})")
        
        if not self.navigate_to_cs_search(institution_code):
            return []
        
        self.set_summer_2025_term()
        
        if not self.click_search_button():
            return []
        
        courses = self.extract_course_data(institution_code, institution_name)
        logger.info(f"Found {len(courses)} CS courses")
        
        try:
            self.driver.switch_to.default_content()
        except:
            pass
        
        return courses
    
    def scrape_all_institutions(self):
        """Scrape all institutions"""
        all_courses = []
        
        for institution_code in self.wa_institutions.keys():
            try:
                courses = self.scrape_institution(institution_code)
                all_courses.extend(courses)
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Error with {institution_code}: {e}")
                continue
        
        self.courses_data = all_courses
        return all_courses
    
    def save_data(self):
        """Save scraped data"""
        if not self.courses_data:
            return
            
        # Save JSON
        with open("wa_cs_summer2025.json", 'w', encoding='utf-8') as f:
            json.dump(self.courses_data, f, indent=2)
        
        # Save CSV
        if self.courses_data:
            keys = set()
            for course in self.courses_data:
                keys.update(course.keys())
            
            with open("wa_cs_summer2025.csv", 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=sorted(keys))
                writer.writeheader()
                writer.writerows(self.courses_data)
        
        logger.info("Data saved to wa_cs_summer2025.json and wa_cs_summer2025.csv")
    
    def print_summary(self):
        """Print summary"""
        if not self.courses_data:
            print("No CS courses found")
            return
        
        print(f"\nTotal CS courses: {len(self.courses_data)}")
        
        by_institution = {}
        for course in self.courses_data:
            name = course.get('institution_name', 'Unknown')
            by_institution[name] = by_institution.get(name, 0) + 1
        
        for name, count in sorted(by_institution.items()):
            if count > 0:
                print(f"  {name}: {count}")

def main():
    print("CTC Link CS Course Scraper")
    print("=" * 30)
    
    headless = input("Run headless? (y/n): ").lower() == 'y'
    
    scraper = CTCCScourseScraper(headless=headless)
    
    try:
        test_code = input("Test one institution? Enter code (e.g. WA080) or Enter for all: ").strip()
        
        if test_code and test_code in scraper.wa_institutions:
            courses = scraper.scrape_institution(test_code)
            scraper.courses_data = courses
        else:
            courses = scraper.scrape_all_institutions()
        
        if courses:
            scraper.save_data()
            scraper.print_summary()
            
            print("\nSample courses:")
            for i, course in enumerate(courses[:3]):
                print(f"{i+1}. {course}")
        else:
            print("No courses found")
    
    finally:
        scraper.close_driver()

if __name__ == "__main__":
    main() 